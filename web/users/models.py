from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError
from django.db import models

from europaea.id import generate_id
from europaea.urwid import get_width
from users.hashers import check_password, make_password


class User(models.Model):
    uid = models.CharField(max_length=5, primary_key=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, max_length=40)
    qq = models.CharField(blank=True, max_length=11)
    line = models.CharField(blank=True, max_length=30)
    groups = pg_fields.ArrayField(models.IntegerField(),
                                  default=list,
                                  size=5)
    cancelled_count = models.IntegerField(default=0)
    last_access = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    is_anonymous = False
    is_authenticated = True

    def clean_name(self):
        name = self.cleaned_data['name']
        if get_width(name) > 16:
            raise ValidationError('the name is too long')

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = generate_id(5)
            if self.email and (self.qq or self.line):
                self.is_active = True
        return super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.name}({self.uid})'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        # del token
        return True

    def check_password(self, raw_password):
        return check_password(raw_password, self.password, self.set_password)
