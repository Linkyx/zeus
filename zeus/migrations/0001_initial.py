# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField(default=False, verbose_name='\u6d88\u606f\u72b6\u6001')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='\u6d88\u606f\u6807\u9898', blank=True)),
                ('content', models.CharField(max_length=255, null=True, verbose_name='\u6d88\u606f\u5185\u5bb9', blank=True)),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('receiver', models.CharField(max_length=255, null=True, verbose_name='\u63a5\u6536\u8005', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u672a\u5220\u9664')),
            ],
            options={
                'verbose_name': '\u6d88\u606f\u4fe1\u606f',
                'verbose_name_plural': '\u6d88\u606f\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='\u9879\u76ee\u540d', blank=True)),
                ('introduction', models.CharField(max_length=255, null=True, verbose_name='\u9879\u76ee\u7b80\u4ecb', blank=True)),
                ('owner', models.CharField(max_length=32, null=True, verbose_name='\u9879\u76ee\u62e5\u6709\u8005', blank=True)),
                ('participant', models.CharField(max_length=32, null=True, verbose_name='\u9879\u76ee\u53c2\u4e0e\u8005', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u672a\u5220\u9664')),
            ],
            options={
                'verbose_name': '\u9879\u76ee\u4fe1\u606f',
                'verbose_name_plural': '\u9879\u76ee\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='\u4efb\u52a1\u540d', blank=True)),
                ('introduction', models.CharField(max_length=255, null=True, verbose_name='\u4efb\u52a1\u7b80\u4ecb', blank=True)),
                ('owner', models.CharField(max_length=32, null=True, verbose_name='\u4efb\u52a1\u62e5\u6709\u8005', blank=True)),
                ('participant', models.CharField(max_length=32, null=True, verbose_name='\u4efb\u52a1\u53c2\u4e0e\u8005', blank=True)),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('finish_time', models.DateTimeField(null=True, verbose_name='\u5b8c\u6210\u65f6\u95f4', blank=True)),
                ('status', models.CharField(default=0, max_length=16, verbose_name='\u5f53\u524d\u72b6\u6001', choices=[(0, '\u5f85\u5904\u7406'), (1, '\u8fdb\u884c\u4e2d'), (2, '\u5df2\u5b8c\u6210')])),
                ('level', models.CharField(default=0, max_length=16, verbose_name='\u4efb\u52a1\u7ea7\u522b', choices=[(0, '\u4f4e'), (1, '\u4e2d'), (2, '\u9ad8')])),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u672a\u5220\u9664')),
                ('project', models.ForeignKey(to='zeus.Project')),
            ],
            options={
                'verbose_name': '\u9700\u6c42\u4fe1\u606f',
                'verbose_name_plural': '\u9700\u6c42\u4fe1\u606f',
            },
        ),
    ]
