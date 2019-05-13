from django.db import models

from europaea.id import generate_id


class Project(models.Model):
    pid = models.CharField(max_length=7, primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    doc_url = models.CharField(max_length=30)
    note = models.TextField(default='')
    pics_count = models.IntegerField(default=0)
    words_count = models.IntegerField(default=0)
    audio_length = models.IntegerField(default=0)
    finish_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pid:
            self.pid = generate_id(7)
            super().save(*args, **kwargs)
            Progress.objects.create(project=self)
            return None
        return super().save(*args, **kwargs)


# 后期开始预处理的时候 记录日期但不记时 正式开始的时候 d7_start的时间相当于开始时间


class Progress(models.Model):
    STATE = (
        (0, 'vanilla'),         # 项目创建
        (-1, 'preprocessing'),  # 后期开始但配音未完成
        (-2, 'waiting'),
        (2, 'recruiting'),      # 项目缺人
        (3, 'processing'),      # 不缺人但未完成
        (4, 'done'),            # 项目完成
        (-10, 'resetted')       # 特殊
    )

    project = models.OneToOneField(Project,
                                   on_delete=models.CASCADE,
                                   primary_key=True)

    d4_state = models.IntegerField(choices=STATE, default=0)
    d5_state = models.IntegerField(choices=STATE, default=-2)
    d6_state = models.IntegerField(choices=STATE, default=-2)
    d7_state = models.IntegerField(choices=STATE, default=-2)

    d4_start = models.DateTimeField(blank=True, null=True)
    d5_start = models.DateTimeField(blank=True, null=True)
    d6_start = models.DateTimeField(blank=True, null=True)
    d7_start = models.DateTimeField(blank=True, null=True)

    metadata = models.TextField()  # jsonfield
