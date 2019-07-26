from hashlib import sha3_256
from os.path import splitext

import magic
from django.conf import settings
from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.functions import Now

from europaea.audio import get_audio_info
from europaea.choices import FILE_TYPE
from europaea.files import mime_to_ftype
from europaea.id import generate_id

fs_cf = FileSystemStorage(location=f'{settings.BASE_DIR}/../file/cf')


class CommitsManager(models.Manager):
    def create(self, work, cfile):
        if work.state != 0:
            raise ValidationError('not allowed to upload in this state')

        cfile.file.seek(0)
        fingerprint = sha3_256(cfile.file.read()).hexdigest()[:32]
        cfile.file.seek(0)
        mime = magic.from_buffer(cfile.file.read(), mime=True)
        cfile.file.seek(0)
        ftype = mime_to_ftype(mime)
        if ftype == 0:
            raise ValidationError('invalid file type')
        cfile.name = f'{work.project}-{work.dep}-{work.role}-{work.user}{splitext(cfile.name)[-1]}'
        metadata = get_audio_info(cfile) if ftype // 10 == 5 else None

        work.state = 1
        # schedule-
        if ftype // 10 == 5:
            work.project.audio_length += metadata['duration']
            work.project.save()

        commits = super().create(cid=generate_id(15),
                                 work=work,
                                 ftype=ftype,
                                 fingerprint=fingerprint,
                                 cfile=cfile)
        return commits


class Commit(models.Model):
    fingerprint = models.CharField(max_length=32, primary_key=True)
    work = models.ForeignKey('works.Work', on_delete=models.CASCADE)
    ftype = models.IntegerField(choices=FILE_TYPE)
    timestamp = models.DateTimeField(auto_now_add=True)
    cfile = models.FileField(storage=fs_cf)
    active = models.BooleanField(default=True)
    metadata = pg_fields.JSONField(default=dict)

    objects = CommitsManager()

    class Meta:
        db_table = 'commit'

    def delete(self, *args, **kwargs):
        if self.work.state != 1:
            raise ValidationError('not allowed to delete in this state')
        self.work.state = 0
        # schedule+
        # delete file
        self.active = False
        self.metadata['del@'] = Now()
        if self.ftype // 10 == 5:
            self.work.project.audio_length -= self.metadata['duration']
            self.work.project.save()
        return None
