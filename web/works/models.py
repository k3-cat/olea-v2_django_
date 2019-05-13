from django.db import models
from django.contrib.postgres import fields as pg_fields

from europaea.id import generate_id
from projects.models import Project
from users.models import User


class Work(models.Model):
    WORKSTATE = (
        (0, 'normal'),
        (1, 'finished'),
        (-1, 'cancelled'),
    )
    DEPARTMENT = (
        (40, 'writing'),
        (50, 'reading'),
        (51, 'reading_eng'),
        (60, 'painting'),
        (70, 'post-production')
    )
    wid = models.CharField(max_length=12, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    dep = models.IntegerField(choices=DEPARTMENT)
    role = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.IntegerField(choices=WORKSTATE, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = pg_fields.JSONField(default=dict)

    class Meta:
        ordering = ('timestamp',)
        unique_together = ('project', 'dep', 'role')

    def save(self, *args, **kwargs):
        if not self.wid:
            self.wid = generate_id(12)
        return super(Work, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        roles_pools = self.project.progress.metadata['roles_pools']
        roles_pools[self.dep].append(self.role)
        super(Work, self).delete(*args, **kwargs)
