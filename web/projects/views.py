from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectNSerializer, ProjectSerializer


class ProjectNAPIView(mixins.CreateModelMixin,
                      viewsets.GenericViewSet): # yapf: disable
    queryset = Project.objects.all()
    lookup_field = 'pid'
    serializer_class = ProjectNSerializer

    def create(self, request):
        # if admin
        return super().create(request)


class ProjectAPIView(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet): # yapf: disable
    queryset = Project.objects.all()
    lookup_field = 'pid'
    serializer_class = ProjectSerializer

    def list(self, request):
        # admin
        return super().list(request)

    def retrieve(self, request, pid=None):
        # if admin or user
        pass

    def update(self, request, pid=None):
        # if admin or user
        # if admin check name, group
        return super().update(request, pid=pid)

    def partial_update(self, request, pid=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
