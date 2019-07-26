from rest_framework import serializers


class ProjectNSerializer(serializers.ModelSerializer):
    base = serializers.CharField(write_only=True)
    pub_date = serializers.CharField(write_only=True)
    ext = serializers.CharField(write_only=True)

    class Meta:
        model = 'projects.Project'
        fields = ('pid', 'base', 'pub_date', 'category', 'ext', 'note')
        read_only_fields = ('pid', )

    def validate(self, attrs):
        attrs['ver'] = 0
        return attrs
