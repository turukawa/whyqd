# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0005_auto_20150119_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='chapterformat',
            field=jsonfield.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='novel',
            name='defaultcurrency',
            field=models.CharField(default=b'gbp', max_length=7, choices=[(b'gbp', b'&pound;'), (b'usd', b'$'), (b'eur', b'&euro;')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='novel',
            name='defaultprice',
            field=models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='novel',
            name='discountpercent',
            field=models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='novel',
            name='discountvolume',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='novel',
            name='lenddays',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='novel',
            name='lendnumber',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
