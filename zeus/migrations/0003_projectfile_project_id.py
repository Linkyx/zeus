# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zeus', '0002_projectfile_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='project_id',
            field=models.CharField(max_length=32, null=True, verbose_name='\u9879\u76eeid', blank=True),
        ),
    ]
