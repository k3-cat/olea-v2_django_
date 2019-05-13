from rest_framework import serializers
from .models import Work


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('wid', 'project', 'dep', 'role', 'user', 'state', 'timestamp', 'metadata')
        read_only_fields = ('wid', 'state', 'timestamp', 'metadata')
