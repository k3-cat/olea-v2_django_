from rest_framework import mixins, viewsets

from bills.models import Application

from ..serializers.bills import JournalSerializer


class JournalView(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):  # yapf: disable
    lookup_field = 'jid'
    lookup_value_regex = '[A-Za-z0-9_-]{12}'
    queryset = Application.objects.all()
    serializer_class = JournalSerializer

    # list
    # create
