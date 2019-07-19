from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import (ProjectNSerializer, ProjectSerializer,
                                  ProjectUSerializer)


class ProjectListView(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    serializer_class = ProjectSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('progress__d5_state', 'progress__d6_state',
                        'progress__d7_state', 'finish_at')
    search_fields = ('title',)

    def get_queryset(self):
        queryset = Project.objects.filter(finish_at=None)
        dep = self.request.query_params.get('dep', None)
        if dep:
            queryset = queryset.filter(project__username=2)
        return queryset


class ProjectView(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):  # yapf: disable

    queryset = Project.objects.filter(finish_at=None)
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

    def retrieve(self, request, pid=None):
        # if admin or user
        return super().retrieve(request, pid)

    def update(self, request, pid=None):
        # if admin or user
        # if admin check name, group
        return super().update(request, pid=pid)

    def partial_update(self, request, pid=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
