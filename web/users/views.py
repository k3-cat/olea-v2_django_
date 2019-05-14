from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import User
from .serializers import UserNSerializer, UserSerializer
from .permissions import UserPermissions, UserNPermissions


class UserAPIView(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet): # yapf: disable
    queryset = User.objects.all()
    lookup_field = 'uid'
    serializer_class = UserSerializer
    # permission_classes = (UserPermissions,)

    def retrieve(self, request, uid=None):
        # if admin or user
        return super().retrieve(request, uid=uid)

    def update(self, request, uid=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
        # if admin or user

    def partial_update(self, request, uid=None):
        return super().partial_update(request, uid=uid)


class UserNAPIView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet): # yapf: disable
    queryset = User.objects.all()
    lookup_field = 'uid'
    serializer_class = UserNSerializer
    # permission_classes = (UserNPermissions,)

    def create(self, request):
        # if admin
        return super().create(request)

    def update(self, request, uid=None):
        # if admin
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def partial_update(self, request, uid=None):
        return super().partial_update(request, uid=uid)
