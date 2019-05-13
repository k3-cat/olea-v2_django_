from django.db import models
from django.contrib.postgres import fields as pg_fields

from europaea.id import generate_id

from .hashers import check_password, make_password


class User(models.Model):
    uid = models.CharField(max_length=5, primary_key=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True, max_length=40)
    qq = models.CharField(blank=True, null=True, max_length=11)
    line = models.CharField(blank=True, null=True, max_length=30)
    groups = pg_fields.ArrayField(models.IntegerField(),
                                  default=list,
                                  size=5)
    cancelled_count = models.IntegerField(default=0)
    last_access = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    is_anonymous = False
    is_authenticated = True

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = generate_id(5)
            if self.email and (self.qq or self.line):
                self.is_active = True
        return super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        full_name = f'{self.name}({self.uid})'
        return full_name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        return True

    def check_password(self, raw_password):
        return check_password(raw_password, self.password, self.set_password)
