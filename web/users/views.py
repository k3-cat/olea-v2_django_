from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .permissions import UserNPermissions, UserPermissions
from .serializers import UserNSerializer, UserSerializer


class UserAPIView(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet): # yapf: disable
    queryset = User.objects.all()
    lookup_field = 'uid'
    lookup_value_regex = '[A-Za-z0-9_-]{5}'
    # permission_classes = (UserPermissions,)

    def get_serializer_class(self):
        if self.action in ('create', 'n_update'):
            return UserNSerializer
        return UserSerializer

    def retrieve(self, request, uid=None):
        # if admin or user
        return super().retrieve(request, uid=uid)

    def update(self, request, uid=None):
        return super().update(request, uid=uid)

    def partial_update(self, request, uid=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def n_create(self, request):
        # if admin
        return super().create(request)

    @action(detail=True, methods=['post'])
    def n_update(self, request, uid=None):
        # if admins
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
