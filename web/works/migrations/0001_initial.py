# Generated by Django 2.2.1 on 2019-05-12 03:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Work',
            fields=[
                ('wid', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('dep', models.IntegerField(choices=[(40, 'writing'), (50, 'reading'), (51, 'reading_eng'), (60, 'painting'), (70, 'post-production')])),
                ('role', models.CharField(max_length=20)),
                ('state', models.IntegerField(choices=[(0, 'normal'), (1, 'finished'), (-1, 'cancelled')], default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('metadata', models.TextField(editable=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('timestamp',),
                'unique_together': {('project', 'dep', 'role')},
            },
        ),
    ]