from rest_framework import mixins, viewsets

from projects.models import Project

from ..serializers.projects import ProjectNSerializer


class ProjectView(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):  # yapf: disable
    queryset = Project.objects.filter(finish_at=None)
    lookup_field = 'pid'
    lookup_value_regex = '[A-Za-z0-9_-]{9}'
    serializer_class = ProjectNSerializer
