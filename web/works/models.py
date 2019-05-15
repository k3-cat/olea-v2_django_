import datetime

from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError
from django.db import models

from europaea.choices import DEPARTMENT, WORKSTATE
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

    def clean(self):
        if self.role not in self.project.progress.roles[self.dep]:
            raise ValidationError(f'role({self.role}) does not exist')
        if getattr(self.project.progress, f'{self.dep/10}_state') < 0:
            raise ValidationError('keep waiting')

    def save(self, *args, **kwargs):
        if not self.wid:
            self.wid = generate_id(12)
            self.project.progress.roles[kwargs["dep"]].remove(kwargs['role'])
            if not self.project.progress.roles[kwargs["dep"]]:
                setattr(self.project.progress, f'{kwargs["dep"]}_state', 2)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.project.progress.roles[self.dep].append(self.role)
        self.state = -2 if 'force' in kwargs else - 1
        self.note += f'c: {datetime.datetime.utcnow().isoformat()}\n'
        self.save()
        return None
