from rest_framework import serializers
from .models import User


class UserNSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'email', 'qq', 'line', 'groups', 'is_active')
        read_only_fields = ('uid',)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password('O3O')
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'email', 'qq', 'line', 'groups',
                  'last_access', 'cancelled_count', 'is_active', 'tasks',
                  'msg_box')
        read_only_fields = ('uid', 'name', 'groups', 'last_access', 'cancelled_count',
                            'is_active', 'tasks', 'msg_box')
        extra_kwargs = {'password': {'write_only': True}}
