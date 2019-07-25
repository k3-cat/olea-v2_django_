import re

from rest_framework import serializers

from bills.models import Apply


class AmmountField(serializers.Field):
    def to_representation(self, value):
        value = str(value)
        return f'{value[:-2]}.{value[-2:]}'

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('incorrect_type', input_type=type(data).__name__)
        if '.' not in data:
            data += '.00'
        if not re.match(r'^-?[0-9]+\.[0-9]{2}$', data):
            self.fail('incorrect_format')

        data = data.strip('.')
        return int(data)


class ApplySerializer(serializers.ModelSerializer):
    ammount = AmmountField()

    class Meta:
        model = Apply
        fields = '__all__'
        read_only_fields = ('aid', )
