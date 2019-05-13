import datetime

from django.core.cache import cache
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import BaseAuthentication

from .models import Token


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class TokenAuthentication(BaseAuthentication):
    model = Token

    def authenticate(self, request):
        auth = get_authorization_header(request)

        if not auth:
            return None
        try:
            token = auth.decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        token_cache = 'token_' + key
        user = cache.get(token_cache)
        if user:
            return user

        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token does not exist.')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('The user is deactived.')

        now = datetime.datetime.utcnow()
        if token.created < now - datetime.timedelta(days=180):
            raise exceptions.AuthenticationFailed('This token is expired.')

        cache.set(token_cache, token.user, 86400*5)

        return (token.user, token)

    def authenticate_header(self, request):
        return 'Token'
