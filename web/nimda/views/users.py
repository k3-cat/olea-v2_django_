from rest_framework import mixins, viewsets

from nimda.serializers.users import UserNSerializer
from users.models import User

class UserNView(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet): # yapf: disable
    queryset = User.objects.all()
    serializer_class = UserNSerializer
    lookup_field = 'uid'

# admin
#    def create(self, request):
