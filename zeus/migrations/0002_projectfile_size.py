# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zeus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='size',
            field=models.CharField(max_length=255, null=True, verbose_name='\u6587\u4ef6\u5927\u5c0f', blank=True),
        ),
    ]
