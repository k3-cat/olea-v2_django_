from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from users.models import User
from users.permissions import UserNPermissions, UserPermissions
from users.serializers import UserNSerializer, UserSerializer


class UserListView(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('is_active',)
    search_fields = ('name', '^email', '^qq', 'line')

    def get_queryset(self):
        queryset = User.objects.all()
        groups = [
            int(v)
            for v in self.request.query_params.get('groups', None).split(';')
        ]
        if groups:
            queryset = queryset.filters(groups__contains=groups)
        return queryset


class UserView(mixins.CreateModelMixin,
               mixins.UpdateModelMixin,
               mixins.RetrieveModelMixin,
               viewsets.GenericViewSet): # yapf: disable
    lookup_field = 'uid'
    lookup_value_regex = '[A-Za-z0-9_-]{5}'
    # permission_classes = (UserPermissions,)

    def get_queryset(self):
        queryset = User.objects.all()
        if not self.request.user.is_nimda():
            queryset = queryset.filters(uid=self.request.user.uid)
        return queryset

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return UserNSerializer
        return UserSerializer

    # def retrieve(self, request, uid=None):

    def update(self, request, uid=None):
        if not request.user.is_nimda():
            request.data.pop('name', None)
            request.data.pop('groups', None)
        return super().update(request, uid=uid)

    def partial_update(self, request, uid=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def create(self, request):
        # if admin
        return super().create(request)


class UserGView():
    pass
