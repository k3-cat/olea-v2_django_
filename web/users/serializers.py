from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'qq', 'line', 'groups',
                  'last_access', 'cancelled_count', 'is_active')
        read_only_fields = fields


class UserESerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'qq', 'line')
        read_only_fields = ('uid',)
