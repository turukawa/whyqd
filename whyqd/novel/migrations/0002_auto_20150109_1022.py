# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='charge',
            field=jsonfield.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='token',
            name='price',
            field=models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
    ]
