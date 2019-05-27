from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from works.models import Work
from works.serializers import (WorkCSerializer, WorkDSerializer,
                               WorkFSerializer, WorkSerializer)


class WorkAPIView(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):  # yapf: disable

    queryset = Work.objects.all()
    lookup_field = 'wid'
    lookup_value_regex = '[A-Za-z0-9_-]{12}'

    def get_serializer_class(self):
        if self.action == 'create':
            return WorkCSerializer
        elif self.action == 'update':
            return WorkFSerializer
        elif self.action == 'destroy':
            return WorkDSerializer
        return WorkSerializer

    def create(self, request):
        # TODO check and alter the user in request if admin
        return super().create(request)

    def retrieve(self, request, wid=None):
        # if admin or own
        return super().retrieve(request, wid=wid)

    def destroy(self, request, wid=None):
        # if admin or own
        # TODO check and alter the user in request if admin
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.cancell()
        return Response(status=status.HTTP_200_OK)

    def update(self, request, wid=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
