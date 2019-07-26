from rest_framework import serializers

from europaea.choices import DEPARTMENT


# TODO new logic
class ProjectUSerializer(serializers.Serializer):
    roles = serializers.ListField(child=serializers.CharField(),
                                  write_only=True)
    dep = serializers.ChoiceField(choices=DEPARTMENT, write_only=True)

    def validate(self, attrs):
        if attrs['dep'] == 60:
            if 60 in attrs['user'].groups or 70 in attrs['user'].groups:
                return attrs
        elif attrs['dep'] in attrs['user'].groups:
            return attrs
        raise serializers.ValidationError(
            f'editing denied for this dep({attrs["dep"]})')

    def perform_update(self, instance, validated_data):
        instance.progress.roles[
            validated_data['dep']] = validated_data['roles']
        if validated_data['roles']:
            setattr(instance.progress, f'd{validated_data["dep"]/10}_state', 1)
        return instance

    def update(self, instance, validated_data):
        return

    def create(self, validated_data):
        return


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'projects.Project'
        fields = '__all__'
        read_only_fields = fields
        depth = 1
