# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiqi', '0004_auto_20160330_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='custom_div',
            field=models.CharField(blank=True, help_text=b'Use html format to enter text.', max_length=500, verbose_name=b'Custom Div'),
        ),
    ]
