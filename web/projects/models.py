from django.contrib.postgres import fields as pg_fields
from django.db import models

from europaea.choices import PROGRESS_STATE
from europaea.id import generate_id


class Project(models.Model):
    pid = models.CharField(max_length=8, primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    doc_url = models.CharField(max_length=30)
    note = models.TextField(default='')
    pics_count = models.IntegerField(default=0)
    words_count = models.IntegerField(default=0)
    audio_length = models.IntegerField(default=0)
    finish_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pid:
            self.pid = generate_id(8)
            super().save(*args, **kwargs)
            Progress.objects.create(project=self)
            return None
        return super().save(*args, **kwargs)


# 后期开始预处理的时候 记录日期但不记时 正式开始的时候 d7_start的时间相当于开始时间
class Progress(models.Model):
    project = models.OneToOneField(Project,
                                   on_delete=models.CASCADE,
                                   primary_key=True)

    d5_state = models.IntegerField(choices=PROGRESS_STATE, default=0)
    d6_state = models.IntegerField(choices=PROGRESS_STATE, default=0)
    d7_state = models.IntegerField(choices=PROGRESS_STATE, default=0)

    d5_start = models.DateTimeField(blank=True, null=True)
    d6_start = models.DateTimeField(blank=True, null=True)
    d7_start = models.DateTimeField(blank=True, null=True)

    roles = pg_fields.JSONField(default=dict)
