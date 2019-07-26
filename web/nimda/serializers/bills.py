from rest_framework import serializers

from bills.serializers import AmmountField


class JournalSerializer(serializers.ModelSerializer):
    credit = AmmountField()
    debit = AmmountField()

    class Meta:
        model = 'bills.Journal'
        fields = '__all__'
        read_only_fields = ('jid', )
