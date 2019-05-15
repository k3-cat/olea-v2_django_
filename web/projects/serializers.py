from rest_framework import serializers

from europaea.choices import DEPARTMENT
from projects.models import Progress, Project


# TODO modify this to use auto title
def auto_title(info):
    return info.split(';')


class ProjectNSerializer(serializers.ModelSerializer):
    eng = serializers.BooleanField(default=False, write_only=True)
    info = serializers.CharField(write_only=True)

    class Meta:
        model = Project
        # title and doc_url fields are only here to displace the results
        fields = ('pid', 'info', 'eng' 'note', 'title', 'doc_url')
        read_only_fields = ('pid', 'title', 'doc_url')

    def validate(self, data):
        data['title'], data['doc_url'] = auto_title(data['info'])
        data.pop('info', None)

    def create(self, validated_data):

        return super().create(validated_data)

    def perform_create(self, validated_data):
        project = super().perform_create(validated_data)
        if validated_data['eng']:
            Progress.objects.create(project=project,
                                    roels={
                                        '40': ['主笔'],
                                        '51': ['FA'],
                                        '60': [],
                                        '70': ['FA'],
                                    })
        else:
            Progress.objects.create(project=project,
                                    roels={
                                        '40': ['主笔'],
                                        '50': ['FA'],
                                        '60': [],
                                        '70': ['FA'],
                                    })
        return project


class ProjectSerializer(serializers.ModelSerializer):
    roles = serializers.JSONField(write_only=True)
    dep = serializers.ChoiceField(choices=DEPARTMENT, write_only=True)

    class Meta:
        model = Project
        fields = ('pid', 'title', 'doc_url', 'progress', 'note', 'pics_count',
                  'words_count', 'audio_length', 'finish_at', 'roles', 'dep')
        read_only_fields = fields
        depth = 1

    def validate(self, data):
        # TODO check if user joined if user in group 60, ignore
        if data['dep'] == 60:
            if 60 in data['user'].groups or 70 in data['user'].groups:
                return data
        elif data['dep'] in data['user'].groups:
            return data
        raise serializers.ValidationError(
            f'editing denied for this dep({data["dep"]})')

    def validate_roles(self, value):
        if isinstance(value, list):
            for role in value:
                if not isinstance(role, str):
                    break
            else:
                return value
        raise serializers.ValidationError(' ')

    def update(self, instance, validated_data):
        # TODO if admin alter user in request
        # if user is FA
        return super().update(instance, validated_data)

    def perform_update(self, instance, validated_data):
        instance.progress.roles[
            validated_data['dep']] = validated_data['roles']
        if validated_data['roles']:
            setattr(instance.progress, f'{validated_data["dep"]}_state', 1)
        validated_data = dict()
        return super().perform_update(self, instance, validated_data)
