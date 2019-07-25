from rest_framework import serializers

from europaea.choices import DEPARTMENT

from projects.info_builder import get_info
from projects.models import Project


class ProjectNSerializer(serializers.ModelSerializer):
    base = serializers.CharField(write_only=True)
    pub_date = serializers.CharField(write_only=True)
    ext = serializers.CharField(write_only=True)

    class Meta:
        model = Project
        fields = ('pid', 'base', 'pub_date', 'category', 'ext', 'note')
        read_only_fields = ('pid',)

    def validate(self, attrs):
        attrs['ver'] = 0
        return get_info(attrs)

    def create(self, validated_data):
        eng = validated_data.pop('eng')
        project = super().create(validated_data)
        project.progress.roles = dict([
            ('60', []),
            ('70', ['FA']),
            ] + [('50', ['FA']) if not eng else('51', ['FA'])])
        project.progress.save()
        return project


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
        instance.progress.roles[validated_data['dep']] = validated_data['roles']
        if validated_data['roles']:
            setattr(instance.progress, f'd{validated_data["dep"]/10}_state', 1)
        return instance

    def update(self, instance, validated_data):
        return

    def create(self, validated_data):
        return


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = fields
        depth = 1
