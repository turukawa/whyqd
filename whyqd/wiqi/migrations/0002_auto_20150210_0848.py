# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiqi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='reverted_from_content_type',
            field=models.ForeignKey(related_name='wiqi_text_reverted_from', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='text',
            name='reverted_from_object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
