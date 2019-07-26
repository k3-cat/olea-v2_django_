from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models

from europaea.id import generate_id, generate_jid

fs_ap = FileSystemStorage(location=f'{settings.BASE_DIR}/../file/ap')


class Application(models.Model):
    wid = models.CharField(max_length=12, primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    reason = models.CharField(max_length=300)
    proof = models.ImageField(storage=fs_ap)
    ammount = models.IntegerField()

    class Meta:
        db_table = 'application'

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

    class Meta:
        db_table = 'journal'
        ordering = ('timestamp', )

    def save(self, *args, **kwargs):
        if not Journal.objects.get(jid=self.pervious).exists():
            raise ValidationError('invalid pervious jid')

        if self._state.adding:
            self.jid = generate_jid(debit=self.debit,
                                    credit=self.credit,
                                    reason=self.reason,
                                    pervious=self.pervious,
                                    timestamp=self.timestamp)
            return super().save(*args, **kwargs)
        raise Exception('cannot edit a journal after created')
