import datetime

from django.db.models.functions import Now
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from o3o_auth.backends import O3oBackend
from o3o_auth.models import Token
from o3o_auth.serializers import AuthLogin, AuthRefresh


def authenticate(request=None, **credentials):
    """
    If the given credentials are valid, return a User object.
    """
    try:
        user = O3oBackend.authenticate(request, **credentials)
    except PermissionError:
        # This backend says to stop in our tracks - this user should not be allowed in at all.
        return None
    # Annotate the user object with the path of the backend.
    user.backend = 'o3o_auth.backends.O3oBackend'
    return user


class AuthView(viewsets.GenericViewSet):
    permission_classes = ()


    def get_serializer(self):
        if self.action == 'login':
            return AuthLogin
        if self.action == 'refresh':
            return AuthRefresh
        raise Exception('impossible')

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


    def logout(self, request):
        pass

    def refresh(self, request):
        token_ = request.data['token']
        token = Token.objects.get(key=token_)

        shifted_now = Now() - datetime.timedelta(days=5)
        if token.created < shifted_now < token.created + datetime.timedelta(days=4):
            token.save()

    def change_password(self, request):
        pass
