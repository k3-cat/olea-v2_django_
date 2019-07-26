from rest_framework import serializers


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'commits.Commit'
        fields = ('work', 'file')
