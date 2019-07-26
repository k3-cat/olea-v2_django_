from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import ProjectSerializer, ProjectUSerializer


class ProjectListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProjectSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('progress__d5_state', 'progress__d6_state',
                        'progress__d7_state')
    search_fields = ('title', )

    def get_queryset(self):
        queryset = Project.objects.filter(finish_at=None)
        dep = self.request.query_params.get('dep', None)
        if dep:
            queryset = queryset.filter(project__username=2)
        return queryset


class ProjectView(mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):  # yapf: disable
    lookup_field = 'pid'
    lookup_value_regex = '[A-Za-z0-9_-]{9}'
    serializer_class = ProjectUSerializer

    def get_queryset(self):
        # only one's projects
        pass

    # def update(self, request, pid=None):

    def partial_update(self, request, pid=None):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
