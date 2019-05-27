from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import (ProjectNSerializer, ProjectSerializer,
                                  ProjectUSerializer)


class ProjectAPIView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet): # yapf: disable
    queryset = Project.objects.all()
    lookup_field = 'pid'
    lookup_value_regex = '[A-Za-z0-9_-]{8}'

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectNSerializer
        if self.action == 'update':
            return ProjectUSerializer
        return ProjectSerializer

    def create(self, request):
        # if admin
        return super().create(request)

    def list(self, request):
        # admin
        return super().list(request)

    def retrieve(self, request, pid=None):
        # if admin or user
        return super().retrieve(request, pid)

    def update(self, request, pid=None):
        # if admin or user
        # if admin check name, group
        return super().update(request, pid=pid)

    def partial_update(self, request, pid=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
