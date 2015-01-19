# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0004_auto_20150118_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='surl',
            field=models.CharField(unique=True, max_length=25, verbose_name=b'Short URL'),
            preserve_default=True,
        ),
    ]
