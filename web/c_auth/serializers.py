from rest_framework import serializers

class AuthLogin(serializers.Serializer):
    name = serializers.CharField(max_length=16)
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        name = attrs.get('name')
        password = attrs.get('password')

        if name and password:
            user = authenticate(request=self.context.get('request'),
                                name=name,
                                password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class AuthRefresh(serializers.Serializer):
    token = serializers.CharField(max_length=42)
