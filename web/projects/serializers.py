from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('pid', 'title', 'doc_url', 'progress', 'note', 'pics_count',
                  'words_count', 'audio_length', 'finish_at')
        read_only_fields = ('pid', 'progress', 'pics_count', 'words_count', 'audio_length', 'finish_at')
