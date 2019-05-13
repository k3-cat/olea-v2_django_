from rest_framework import serializers
from .models import Storage


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('work', 'content_type', 'fingerprint', 'uploaded', 'metadata')
        read_only_fields = ('work', 'content_type', 'fingerprint', 'uploaded', 'metadata')
