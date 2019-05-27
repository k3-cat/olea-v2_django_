from hashlib import sha3_256

import magic
from rest_framework import serializers

from europaea import files, audio
from works.models import Work, WorkFile


class WorkCSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('wid', 'project', 'dep', 'role', 'user')
        read_only_fields = ('wid', )


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
            work.work_file.delete()
        if validated_data['cancell_work']:
            work.delete()
        return work


class WorkFSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = WorkFile
        fields = ('work', 'file')

    def validate(self, attrs):
        file_dir = files.get_file_path(attrs['work'])
        files.create_if_not_exist(file_dir)
        hasher = sha3_256()
        type_id = 0
        with open(file_dir, 'wb') as f:
            file_ = attrs.pop('file')
            for i, chunk in enumerate(file_.chunks()):
                if i == 0:
                    mime = magic.from_buffer(chunk, mime=True)
                    type_id = files.mime_to_type_id(mime)
                f.write(chunk)
                hasher.update(chunk)
        attrs['type_id'] = type_id
        attrs['fingerprint'] = hasher.digest()
        attrs['file_dir'] = file_dir
        if type_id == 51:
            attrs['metadata'] = audio.get_info(file_dir)
        return attrs


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'
        read_only_fields = fields
