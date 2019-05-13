from django.db import models
from django.contrib.postgres import fields as pg_fields

from works.models import Work


class Storage(models.Model):
    TYPE_ID = (
        (0, 'none'),
        (10, 'folder'),
        (50, 'audio-wav'),
        (51, 'audio-flac'),
        (52, 'audio-mp3'),
        (60, 'picture-png'),
        (70, 'video-mkv'),
        (71, 'video-mp4'),
    ) # yapf: disable
    work = models.OneToOneField(Work,
                                on_delete=models.CASCADE,
                                primary_key=True)
    type_id = models.IntegerField(choices=TYPE_ID, default=0)
    fingerprint = models.BinaryField(max_length=32, unique=True)  # non editable by default
    uploaded = models.DateTimeField(auto_now_add=True)
    metadata = pg_fields.JSONField(default=dict)
