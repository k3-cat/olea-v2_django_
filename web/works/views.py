from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import Work
from .serializers import WorkSerializer, WorkCSerializer


class WorkCAPIView(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Work.objects.all()
    lookup_field = 'wid'
    serializer_class = WorkCSerializer

    def create(self, request):
        # TODO check and alter the user in request if admin
        return super().create(request)


class WorkAPIView(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet): # yapf: disable
    queryset = Work.objects.all()
    lookup_field = 'wid'
    serializer_class = WorkSerializer

    def retrieve(self, request, wid=None):
        # if admin or own
        return super().retrieve(request, wid=wid)

    def destroy(self, request, wid=None):
        # if admin or own
        # TODO check and alter the user in request if admin
        return super().destroy(request, wid=wid)
