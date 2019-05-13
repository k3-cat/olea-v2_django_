from django.db import models
from django.conf import settings

from europaea.id import generate_id


class Token(models.Model):
    key = models.CharField(max_length=42, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='auth_token',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_pulse = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_id(42)
        return super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return self.key
