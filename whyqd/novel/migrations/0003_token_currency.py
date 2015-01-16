# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0002_auto_20150109_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='currency',
            field=models.CharField(default=b'gbp', max_length=7, choices=[(b'gbp', b'&pound;'), (b'usd', b'$'), (b'eur', b'&euro;')]),
            preserve_default=True,
        ),
    ]
