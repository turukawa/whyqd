# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiqi', '0003_wiqi_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='surl',
            field=models.CharField(unique=True, max_length=16, verbose_name=b'Short URL'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wiqi',
            name='surl',
            field=models.CharField(unique=True, max_length=16, verbose_name=b'Short URL'),
            preserve_default=True,
        ),
    ]
