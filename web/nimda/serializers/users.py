from rest_framework import serializers

from users.models import User


# nimda[&search &self-update]
class UserNSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'qq', 'email', 'line', 'groups')
        read_only_fields = ('uid', )

    def validate(self, attrs):
        if 'name' not in attrs and self.instance.name:
            attrs['name'] = self.instance.name
        return attrs

# TODO new password generation progress
    def perform_create(self, validated_data):
        user = super().create(validated_data)
        user.set_password('O3O')
        user.save()
        return user
