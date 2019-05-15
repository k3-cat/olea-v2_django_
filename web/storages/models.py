from django.contrib.postgres import fields as pg_fields
from django.db import models

from europaea.choices import STORAGE_TYPE
from works.models import Work


class Storage(models.Model):
    work = models.OneToOneField(Work,
                                on_delete=models.CASCADE,
                                primary_key=True)
    type_id = models.IntegerField(choices=STORAGE_TYPE)
    fingerprint = models.BinaryField(max_length=32, unique=True)  # non editable by default
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = pg_fields.JSONField(default=dict)

    def create(self, *args, **kwargs):
        # change state
        return super().create(*args, **kwargs)
