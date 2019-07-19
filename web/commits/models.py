from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Now

from europaea.choices import FILE_TYPE


class Commits(models.Model):
    cid = models.CharField(max_length=12, primary_key=True)
    work = models.ForeignKey('works.Work',
                             on_delete=models.CASCADE)
    type_id = models.IntegerField(choices=FILE_TYPE)
    fingerprint = models.BinaryField(max_length=32,
                                     unique=True)  # non editable by default
    timestamp = models.DateTimeField(auto_now_add=True)
    file_exist = models.BooleanField(default=True)
    metadata = pg_fields.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if self.work.state != 0:
            raise ValidationError('not allowed to upload in this state')
        self.work.state = 1
        # schedule-
        if self.type_id/10 == 5:
            self.work.project.audio_length += self.metadata['duration']
            self.work.project.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.work.state != 1:
            raise ValidationError('not allowed to delete in this state')
        self.work.state = 0
        # schedule+
        # delete file
        self.file_exist = False
        self.metadata['del_time'] = Now()
        if self.type_id / 10 == 5:
            self.work.project.audio_length -= self.metadata['duration']
            self.work.project.save()
        return None
