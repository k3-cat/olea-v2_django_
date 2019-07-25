from rest_framework import serializers

from bills.models import Journal
from bills.serializers import AmmountField


class JournalSerializer(serializers.ModelSerializer):
    credit = AmmountField()
    debit = AmmountField()

    class Meta:
        model = Journal
        fields = '__all__'
        read_only_fields = ('jid', )
