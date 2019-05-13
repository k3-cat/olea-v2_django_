import datetime

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Token
from .backends import O3oBackend


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
    user.backend = 'o3o_auth.O3oBackend'
    return user


@api_view(['POST'])
def login_views(request):
    receive = request.data
    name = receive['name']
    password = receive['password']
    user = authenticate(name=name, password=password)
    if not user:
        return Response({"msg": "User dose not exist or the pawword is invalid."},
                        status=status.HTTP_401_UNAUTHORIZED)

    if user.is_active:
        # revoke the old token
        token = user.token
        if token:
            token.delete()
        token = Token.objects.create(user=user)

        return Response({"token": token}, status=status.HTTP_200_OK)


@api_view(['GET'])
def logout_view(request):
    token_ = request.data['token']
    if not token_:
        return

    token.delete()


@api_view(['PUT'])
def change_password_view(request):
    pass


@api_view(['GET'])
def refresh_view(request):
    token_ = request.data['token']
    token = Token.objects.get(key=token_)

    shifted_now = datetime.datetime.utcnow() - datetime.timedelta(days=5)
    if token.created < shifted_now < token.created + datetime.timedelta(days=4):
        token.save()
