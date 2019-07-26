from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Now

from europaea.choices import DEPARTMENT, WORKSTATE
from europaea.id import generate_id


class WorkManager(models.Manager):
    def create(self, project, dep, user, role):
        if dep not in user.groups:
            raise ValidationError(f'user{user.uid} not in this department({dep})')
        if dep not in project.progress.roles:
            raise ValidationError(f'department({dep}) does not exist in this project')
        if role not in project.progress.roles[dep]:
            raise ValidationError(f'role({role}) does not exist')
        if getattr(project.progress, f'd{dep//10}_state') < 0:
            raise ValidationError(f'department({dep}) still waiting')
        project.progress.roles[dep].remove(role)
        if not project.progress.roles[dep]:
            setattr(project.progress, f'd{dep//10}_state', 2)
        project.progress.save()
        work = super().create(wid=generate_id(15),
                              project=project,
                              dep=dep,
                              user=user,
                              role=role)
        return work


class Work(models.Model):
    wid = models.CharField(max_length=12, primary_key=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    dep = models.IntegerField(choices=DEPARTMENT)
    role = models.CharField(max_length=20)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    state = models.IntegerField(choices=WORKSTATE, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(default='')

    objects = WorkManager()

    class Meta:
        db_table = 'work'
        ordering = ('timestamp',)
        unique_together = ('project', 'dep', 'role')

    def delete(self, *args, **kwargs):
        if self.state != 0:
            raise ValidationError('not allowed to cancell under this state')
        self.project.progress.roles[self.dep//10].append(self.role)
        self.state = -2 if 'force' in kwargs else - 1
        self.note += f'c: {Now()}\n'
        self.project.progress.save()
        self.save()
        return True
