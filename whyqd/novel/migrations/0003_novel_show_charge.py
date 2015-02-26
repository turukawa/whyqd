# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0002_token_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='show_charge',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
