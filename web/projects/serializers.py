from rest_framework import serializers
from .models import Project, Progress


# TODO modify this to use auto title
def auto_title(info):
    result = dict()
    info_ = info.split(';')
    result['title'] = info_[0]
    result['doc_url'] = info_[1]
    return result


class ProjectNSerializer(serializers.ModelSerializer):
    info = serializers.CharField(write_only=True)

    class Meta:
        model = Project
        # title and doc_url fields are only here to displace the results
        fields = ('pid', 'info', 'note', 'title', 'doc_url')
        read_only_fields = ('pid', 'title', 'doc_url')

    def create(self, validated_data):
        validated_data = auto_title(validated_data['info'])
        print(validated_data)
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    roles = serializers.JSONField(write_only=True)
    dep = serializers.CharField(write_only=True)

    class Meta:
        model = Project
        fields = ('pid', 'title', 'doc_url', 'progress', 'note', 'pics_count',
                  'words_count', 'audio_length', 'finish_at', 'roles', 'dep')
        read_only_fields = fields
        depth = 1

    def update(self, instance, validated_data):
        instance.progress.metadata[f'roles-{validated_data["dep"]}'] = validated_data['roles']
        validated_data.pop('roles', None)
        return super().update(instance, validated_data)
