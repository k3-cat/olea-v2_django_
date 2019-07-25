from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Now

from europaea.choices import DEPARTMENT, WORKSTATE
from europaea.id import generate_id


class Work(models.Model):
    wid = models.CharField(max_length=12, primary_key=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    dep = models.IntegerField(choices=DEPARTMENT)
    role = models.CharField(max_length=20)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    state = models.IntegerField(choices=WORKSTATE, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField()

    class Meta:
        ordering = ('timestamp',)
        unique_together = ('project', 'dep', 'role')

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.wid = generate_id(12)
            if self.dep not in self.user.groups:
                raise ValidationError(f'user{self.user.uid} not in this department({self.dep})')
            dep_0 = self.dep//10
            if dep not in self.project.progress.roles:
                raise ValidationError(f'department({dep}) does not exist')
            if self.role not in self.project.progress.roles[dep]:
                raise ValidationError(f'role({self.role}) does not exist')
            if getattr(self.project.progress, f'd{dep_0}_state') < 0:
                raise ValidationError('keep waiting')
            self.project.progress.roles[dep].remove(self.role)
            if not self.project.progress.roles[dep]:
                setattr(self.project.progress, f'd{dep_0}_state', 2)
            self.project.progress.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.state != 0:
            raise ValidationError('not allowed to cancell under this state')
        self.project.progress.roles[self.dep//10].append(self.role)
        self.state = -2 if 'force' in kwargs else - 1
        self.note += f'c: {Now()}\n'
        self.project.progress.save()
        self.save()
        return True
