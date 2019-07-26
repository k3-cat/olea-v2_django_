from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError
from django.db import models

from europaea.id import generate_id
from europaea.urwid import get_width
from users.hashers import check_password, make_password


class UserManager(models.Manager):
    def create(self, name, email, qq, line, group):
        user = super().create(name=name,
                              email=email,
                              qq=qq,
                              line=line,
                              group=group)
        user.uid = generate_id(6)
        user.set_password('OEO')
        if self.email and (self.qq or self.line):
            user.is_active = True
        return user


class User(models.Model):
    uid = models.CharField(max_length=6, primary_key=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, max_length=40)
    qq = models.CharField(blank=True, max_length=11)
    line = models.CharField(blank=True, max_length=30)
    groups = pg_fields.ArrayField(models.IntegerField(), default=list, size=5)
    cancelled_count = models.IntegerField(default=0)
    last_access = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = UserManager()
    is_anonymous = False
    is_authenticated = True

    class Meta:
        db_table = 'c_user'
        ordering = ('name', )

    def save(self, *args, **kwargs):
        if get_width(self.name) > 16:
            raise ValidationError('the name is too long')
        return super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        # TODO del token
        return True

    def check_password(self, raw_password):
        return check_password(raw_password, self.password, self.set_password)
