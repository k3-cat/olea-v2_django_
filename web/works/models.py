from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Now

from europaea.choices import DEPARTMENT, STORAGE_TYPE, WORKSTATE
from europaea.id import generate_id
from projects.models import Project
from users.models import User


class Work(models.Model):
    wid = models.CharField(max_length=12, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    dep = models.IntegerField(choices=DEPARTMENT)
    role = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.IntegerField(choices=WORKSTATE, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField()

    class Meta:
        ordering = ('timestamp',)
        unique_together = ('project', 'dep', 'role')

    def save(self, *args, **kwargs):
        if not self.wid:
            self.wid = generate_id(12)
            if self.dep not in self.user.groups:
                raise ValidationError(f'user{self.user.uid} not in this department({self.dep})')
            dep = str(self.dep)
            if dep not in self.project.progress.roles:
                raise ValidationError(f'department({dep}) does not exist')
            if self.role not in self.project.progress.roles[dep]:
                raise ValidationError(f'role({self.role}) does not exist')
            if getattr(self.project.progress, f'd{dep[0]}_state') < 0:
                raise ValidationError('keep waiting')
            self.project.progress.roles[dep].remove(self.role)
            if not self.project.progress.roles[dep]:
                setattr(self.project.progress, f'd{dep[0]}_state', 2)
            self.project.progress.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.state != 0:
            raise ValidationError('not allowed to cancell under this state')
        dep = str(self.dep)
        self.project.progress.roles[dep].append(self.role)
        self.state = -2 if 'force' in kwargs else - 1
        self.note += f'c: {Now()}\n'
        self.project.progress.save()
        self.save()
        return True


class WorkFile(models.Model):
    work = models.OneToOneField(Work,
                                on_delete=models.CASCADE,
                                primary_key=True)
    type_id = models.IntegerField(choices=STORAGE_TYPE)
    fingerprint = models.BinaryField(max_length=32,
                                     unique=True)  # non editable by default
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = pg_fields.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if self.work.state != 0:
            raise ValidationError('not allowed to upload in this state')
        self.work.state = 1
        # schedule-
        if self.type_id == 51:
            self.work.project.audio_length += self.metadata['duration']
            self.work.project.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.work.state != 1:
            raise ValidationError('not allowed to delete in this state')
        self.work.state = 0
        # schedule+
        if self.type_id == 51:
            self.work.project.audio_length -= self.metadata['duration']
            self.work.project.save()
        return super().delete(*args, **kwargs)
