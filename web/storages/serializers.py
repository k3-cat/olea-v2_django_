from rest_framework import serializers
from .models import Storage


class StorageCSerializer(serializers.ModelSerializer):
    file_ = serializers.FileField(write_only=True)

    class Meta:
        model = Storage
        fields = ('work', )

    def create(self, validated_data):




class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'
        read_only_fields = fields
