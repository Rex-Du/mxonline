# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_lesson_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='url',
        ),
        migrations.AddField(
            model_name='vedio',
            name='url',
            field=models.CharField(default='', max_length=500, verbose_name='播放地址'),
        ),
    ]
