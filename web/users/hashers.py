import importlib
import warnings
from collections import OrderedDict

from .crypto import get_random_string

UNUSABLE_PASSWORD_PREFIX = '!'  # This will never be a valid encoded hash
UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40  # number of random chars to add after UNUSABLE_PASSWORD_PREFIX


def mask_hash(hash_, show=6, char="*"):
    """
    Return the given hash, with only the first ``show`` number shown. The
    rest are masked with ``char`` for security reasons.
    """
    masked = hash_[:show]
    masked += char * len(hash_[show:])
    return masked


class BasePasswordHasher:
    """
    Abstract base class for password hashers

    When creating your own hasher, you need to override algorithm,
    verify(), encode() and safe_summary().

    PasswordHasher objects are immutable.
    """
    algorithm = None
    library = None

    def _load_library(self):
        if self.library is not None:
            if isinstance(self.library, (tuple, list)):
                name, mod_path = self.library
            else:
                mod_path = self.library
            try:
                module = importlib.import_module(mod_path)
            except ImportError as e:
                raise ValueError("Couldn't load %r algorithm library: %s" %
                                 (self.__class__.__name__, e))
            return module
        raise ValueError("Hasher %r doesn't specify a library attribute" %
                         self.__class__.__name__)

    def salt(self):
        """Generate a cryptographically secure nonce salt in ASCII."""
        return get_random_string()

    def verify(self, password, encoded):
        """Check if the given password is correct."""
        raise NotImplementedError(
            'subclasses of BasePasswordHasher must provide a verify() method')

    def encode(self, password, salt):
        """
        Create an encoded database value.

        The result is normally formatted as "algorithm$salt$hash" and
        must be fewer than 128 characters.
        """
        raise NotImplementedError(
            'subclasses of BasePasswordHasher must provide an encode() method')

    def safe_summary(self, encoded):
        """
        Return a summary of safe values.

        The result is a dictionary and will be used where the password field
        must be displayed to construct a safe representation of the password.
        """
        raise NotImplementedError(
            'subclasses of BasePasswordHasher must provide a safe_summary() method'
        )

    def must_update(self, encoded):
        return False

    def harden_runtime(self, password, encoded):
        """
        Bridge the runtime gap between the work factor supplied in `encoded`
        and the work factor suggested by this hasher.

        Taking PBKDF2 as an example, if `encoded` contains 20000 iterations and
        `self.iterations` is 30000, this method should run password through
        another 10000 iterations of PBKDF2. Similar approaches should exist
        for any hasher that has a work factor. If not, this method should be
        defined as a no-op to silence the warning.
        """
        warnings.warn(
            'subclasses of BasePasswordHasher should provide a harden_runtime() method'
        )


class Argon2PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the argon2 algorithm.

    This is the winner of the Password Hashing Competition 2013-2015
    (https://password-hashing.net). It requires the argon2-cffi library which
    depends on native C code and might cause portability issues.
    """
    algorithm = 'argon2'
    library = 'argon2'

    time_cost = 30
    memory_cost = 1024
    parallelism = 2

    def encode(self, password, salt):
        argon2 = self._load_library()
        data = argon2.low_level.hash_secret(
            password.encode(),
            salt.encode(),
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=argon2.DEFAULT_HASH_LENGTH,
            type=argon2.low_level.Type.ID,
        )
        return self.algorithm + data.decode('ascii')

    def verify(self, password, encoded):
        argon2 = self._load_library()
        algorithm, rest = encoded.split('$', 1)
        assert algorithm == self.algorithm
        try:
            return argon2.low_level.verify_secret(
                ('$' + rest).encode('ascii'),
                password.encode(),
                type=argon2.low_level.Type.ID,
            )
        except argon2.exceptions.VerificationError:
            return False

    def safe_summary(self, encoded):
        (algorithm, variety, version, time_cost, memory_cost, parallelism,
         salt, data) = self._decode(encoded)
        assert algorithm == self.algorithm
        return OrderedDict([
            ('algorithm', algorithm),
            ('variety', variety),
            ('version', version),
            ('memory cost', memory_cost),
            ('time cost', time_cost),
            ('parallelism', parallelism),
            ('salt', mask_hash(salt)),
            ('hash', mask_hash(data)),
        ])

    def must_update(self, encoded):
        (algorithm, variety, version, time_cost, memory_cost, parallelism,
         salt, data) = self._decode(encoded)
        assert algorithm == self.algorithm
        argon2 = self._load_library()
        return (argon2.low_level.ARGON2_VERSION != version
                or self.time_cost != time_cost
                or self.memory_cost != memory_cost
                or self.parallelism != parallelism)

    def harden_runtime(self, password, encoded):
        # The runtime for Argon2 is too complicated to implement a sensible
        # hardening algorithm.
        pass

    def _decode(self, encoded):
        """
        Split an encoded hash and return: (
            algorithm, variety, version, time_cost, memory_cost,
            parallelism, salt, data,
        ).
        """
        bits = encoded.split('$')
        if len(bits) == 5:
            # Argon2 < 1.3
            algorithm, variety, raw_params, salt, data = bits
            version = 0x10
        else:
            assert len(bits) == 6
            algorithm, variety, raw_version, raw_params, salt, data = bits
            assert raw_version.startswith('v=')
            version = int(raw_version[len('v='):])
        params = dict(bit.split('=', 1) for bit in raw_params.split(','))
        assert len(params) == 3 and all(x in params for x in ('t', 'm', 'p'))
        time_cost = int(params['t'])
        memory_cost = int(params['m'])
        parallelism = int(params['p'])
        return (
            algorithm,
            variety,
            version,
            time_cost,
            memory_cost,
            parallelism,
            salt,
            data,
        )


def check_password(password, encoded, setter=None):
    """
    Return a boolean of whether the raw password matches the three
    part encoded digest.

    If setter is specified, it'll be called when you need to
    regenerate the password.
    """
    if encoded is None or not encoded.startswith(UNUSABLE_PASSWORD_PREFIX):
        return False

    try:
        hasher = Argon2PasswordHasher
    except ValueError:
        # encoded is gibberish or uses a hasher that's no longer installed.
        return False

    must_update = hasher.must_update(encoded)
    is_correct = hasher.verify(password, encoded)

    if setter and is_correct and must_update:
        setter(password)
    return is_correct


def make_password(password, salt=None, hasher='default'):
    """
    Turn a plain-text password into a hash for database storage

    Same as encode() but generate a new random salt. If password is None then
    return a concatenation of UNUSABLE_PASSWORD_PREFIX and a random string,
    which disallows logins. Additional random string reduces chances of gaining
    access to staff or superuser accounts. See ticket #20079 for more info.
    """
    if password is None:
        return UNUSABLE_PASSWORD_PREFIX + get_random_string(
            UNUSABLE_PASSWORD_SUFFIX_LENGTH)
    hasher = Argon2PasswordHasher()
    salt = salt or hasher.salt()
    return hasher.encode(password, salt)
