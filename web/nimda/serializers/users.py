from rest_framework import serializers


class UserNSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'users.User'
        fields = ('uid', 'name', 'qq', 'email', 'line', 'groups')
        read_only_fields = ('uid', )

    def validate(self, attrs):
        if 'name' not in attrs and self.instance.name:
            attrs['name'] = self.instance.name
        return attrs
