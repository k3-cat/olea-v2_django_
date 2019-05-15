from rest_framework import serializers

from works.models import Work


class WorkCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('wid', 'project', 'dep', 'role', 'user')
        read_only_fields = ('wid', )

    def validate(self, data):
        if data['dep'] not in data['user'].groups:
            raise serializers.ValidationError(
                f'user{data["user"]} not in this department({data["dep"]})')


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'
        read_only_fields = fields
