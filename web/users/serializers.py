from rest_framework import serializers
from .models import User


# nimda[&search &self-update]
class UserNSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'qq', 'email', 'line', 'groups')
        read_only_fields = ('uid',)

    def validate(self, attrs):
        if 'name' not in attrs and self.instance.name:
            attrs['name'] = self.instance.name
        return attrs

    def perform_create(self, validated_data):
        user = super().create(validated_data)
        user.set_password('O3O')
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'qq', 'line', 'groups',
                  'last_access', 'cancelled_count', 'is_active')
        read_only_fields = fields
