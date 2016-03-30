# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 17:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0004_auto_20150226_1256'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='token',
            managers=[
                ('query', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='token',
            name='recipient',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name=b'Email'),
        ),
    ]
