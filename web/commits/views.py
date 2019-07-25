from rest_framework import mixins, viewsets

from commits.serializers import Download, Upload


class CommitsView(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):  # yapf: disable

    lookup_field = 'work'
    lookup_value_regex = '[A-Za-z0-9_-]{12}'

    def get_serializer_class(self):
        if self.action == 'create':
            return Upload
        if self.action == 'retrieve':
            return Download
        raise Exception('this is impossible (commits/views.py)')
