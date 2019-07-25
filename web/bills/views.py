from rest_framework import mixins, viewsets

from bills.models import Apply
from bills.serializers import ApplySerializer


class CommitsView(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):  # yapf: disable

    lookup_field = 'aid'
    lookup_value_regex = '[A-Za-z0-9_-]{12}'
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer

    # list
    # create
