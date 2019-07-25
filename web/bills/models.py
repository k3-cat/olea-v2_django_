from django.core.exceptions import ValidationError
from django.db import models

from europaea.id import generate_id, generate_jid


class Apply(models.Model):
    wid = models.CharField(max_length=12, primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    reason = models.CharField(max_length=300)
    ammount = models.IntegerField()

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.wid = generate_id(12)
            return super().save(*args, **kwargs)
        raise Exception('cannot edit an application after created')


class Journal(models.Model):
    jid = models.CharField(max_length=42, primary_key=True)
    debit = models.IntegerField()
    credit = models.IntegerField()
    reason = models.CharField(max_length=300)
    pervious = models.CharField(max_length=42)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean_reason(self):
        if not self.reason:
            raise ValidationError('reason cannot be empty')

    def clean_pervious(self):
        if not Journal.objects.filter(jid=self.pervious):
            raise ValidationError('invalid pervious jid')

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.jid = generate_jid(debit=self.debit,
                                    credit=self.credit,
                                    reason=self.reason,
                                    pervious=self.pervious,
                                    timestamp=self.timestamp)
            return super().save(*args, **kwargs)
        raise Exception('cannot edit a journal after created')
