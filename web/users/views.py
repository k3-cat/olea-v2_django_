from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from users.models import User
from users.permissions import UserPermissions
from users.serializers import UserESerializer, UserSerializer


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


class UserView(mixins.UpdateModelMixin,
               mixins.RetrieveModelMixin,
               viewsets.GenericViewSet): # yapf: disable
    lookup_field = 'uid'
    serializer_class = UserESerializer
    lookup_value_regex = '[A-Za-z0-9_-]{6}'
    # permission_classes = (UserPermissions,)

    def get_queryset(self):
        return User.objects.all().filters(uid=self.request.user.uid)

    # def retrieve(self, request, uid=None):

    # def update(self, request, uid=None):

    def partial_update(self, request, uid=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
