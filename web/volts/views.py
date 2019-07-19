from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from volts.models import Volt
from volts.serializers import DownVolt



class VoltView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = DownVolt
    queryset = Volt.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}
