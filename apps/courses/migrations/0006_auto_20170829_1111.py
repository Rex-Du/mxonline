# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(max_length=100, verbose_name='课程分类'),
        ),
    ]
