from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'email', 'qq', 'line', 'groups',
                  'last_access', 'cancelled_count', 'is_active')
        read_only_fields = ('uid', 'last_access', 'cancelled_count', 'is_active')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password('O3O')
        user.save()
        return user
