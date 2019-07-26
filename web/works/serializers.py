from rest_framework import serializers


# create
class WorkCSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'works.Work'
        fields = ('wid', 'project', 'dep', 'role', 'user')
        read_only_fields = ('wid', )


# destory
class WorkDSerializer(serializers.Serializer):
    delete_file = serializers.BooleanField(default=False, write_only=True)
    cancell_work = serializers.BooleanField(default=False, write_only=True)

    def cancell(self, **kwargs):
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )
        work = self.instance
        if validated_data['delete_file']:
            work.commits.delete()
        if validated_data['cancell_work']:
            work.delete()
        return work

    def create(self):
        pass

    def update(self):
        pass


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'works.sWork'
        fields = '__all__'
        read_only_fields = fields
