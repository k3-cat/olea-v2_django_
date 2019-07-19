from rest_framework import serializers
from volts.models import Volt


# down_volt
class DownVolt(serializers.ModelSerializer):
    class Meta:
        model = Volt
        fields = '__all__'
        read_only_fields = ('user', 'timestamp')

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs
