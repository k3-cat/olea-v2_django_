from django.db import models
from django.db.models.functions import Now
from django.conf import settings

from europaea.id import generate_id


class TokenManager(models.Manager):
    def create(self, user):
        token = super().create(key=generate_id(42), user=user)
        return token


class Token(models.Model):
    key = models.CharField(max_length=42, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='auth_token',
                                on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_pulse = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'c_token'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.key = generate_id(42)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key

    def refresh(self):
        self.last_pulse = Now()
