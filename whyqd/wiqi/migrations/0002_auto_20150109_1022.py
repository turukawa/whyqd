# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiqi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wiqi',
            name='read_if',
            field=models.CharField(default=b'open', max_length=5, choices=[(b'open', b'Open'), (b'login', b'Login'), (b'own', b'Own')]),
            preserve_default=True,
        ),
    ]
