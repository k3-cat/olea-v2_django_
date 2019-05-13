from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import Work
from .serializers import WorkSerializer


class WorkAPIViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin, mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Work.objects.all()
    lookup_field = 'wid'
    serializer_class = WorkSerializer

    def list(self, request):
        # admin
        return super().list(request)

    def retrieve(self, request, wid=None):
        # if admin or own
        return super().retrieve(request, wid=wid)

    def create(self, request):
        # if amind then use uid in request
        # compare user group and dep in reequest
        # check permission
        return super().create(request)

    def update(self, request, wid=None):
        return super().update(request, wid=wid)

    def partial_update(self, request, wid=None):
        # if amind then use uid in request
        # compare user equal
        # check state
        return super().update(request, wid=wid)

    def destory(self, request, wid=None):
        # id super admin
        return super().destory(request, wid=wid)
