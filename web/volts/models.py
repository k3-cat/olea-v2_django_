from django.db import models


class VoltManager(models.Manager):
    pass

class Volt(models.Model):
    commits = models.OneToOneField('commits.Commits',
                                   on_delete=models.CASCADE,
                                   primary_key=True)
    user = models.OneToOneField('users.User',
                                on_delete=models.CASCADE)
    reason = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = VoltManager()

    class Meta:
        db_table = 'volt'
