# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_teacher_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='level',
            field=models.CharField(choices=[('JPJS', '金牌讲师'), ('YPJS', '银牌讲师'), ('TPJS', '铜牌讲师')], default='YPJS', max_length=4, verbose_name='级别'),
        ),
    ]
