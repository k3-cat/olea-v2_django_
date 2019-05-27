from rest_framework import serializers
from .models import User


class UserNSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'qq', 'email', 'line', 'groups')
        read_only_fields = ('uid',)

    def validate(self, data):
        if 'name' not in data and self.instance.name:
            data['name'] = self.instance.name
        return data

    def perform_create(self, validated_data):
        user = super().create(validated_data)
        user.set_password('O3O')
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'email', 'qq', 'line', 'groups',
                  'last_access', 'cancelled_count', 'is_active')
        read_only_fields = ('uid', 'name', 'groups', 'last_access', 'cancelled_count',
                            'is_active')
