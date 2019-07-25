import random
from hashlib import sha3_512

ID_ALPHABET = ('0123456789aAbBcC'
               'dDeEfFgGhHiIjJkK'
               'lLmMnNoOpPqQrRsS'
               'tTuUvVwWxXyYzZ_-')


def generate_id(k):
    return ''.join(random.choices(ID_ALPHABET, k=k))


def generate_pid(base, pub_date, category, version):
    random.seed = sha3_512(f'{base} {pub_date} {category}').digest()
    pid_ = ''.join(random.choices(ID_ALPHABET, k=8))
    return f'{pid_}{ID_ALPHABET[version]}'


def generate_jid(debit, credit, reason, pervious, timestamp):
    random.seed = sha3_512(
        f'{debit}/{credit}|{reason}-{timestamp}-{pervious}').digest()
    return ''.join(random.choices(ID_ALPHABET, k=40))
