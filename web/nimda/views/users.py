from rest_framework import mixins, viewsets

from users.models import User

from ..serializers.users import UserNSerializer


class UserNView(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet): # yapf: disable
    queryset = User.objects.all()
    serializer_class = UserNSerializer
    lookup_field = 'uid'
