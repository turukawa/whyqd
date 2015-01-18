# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0003_token_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='license',
        ),
        migrations.AddField(
            model_name='novel',
            name='licensing',
            field=models.CharField(default=b'(c)', help_text=b'What form of copyright do you offer?', max_length=50, verbose_name=b'Release License', choices=[(b'(c)', b'All Rights Reserved'), (b'CC0', b'No Rights Reserved'), (b'CC BY', b'CC Attribution'), (b'CC BY-ND', b'CC Attribution + NoDerivatives'), (b'CC BY-SA', b'CC Attribution + ShareAlike'), (b'CC BY-NC', b'CC Attribution + Noncommercial'), (b'CC BY-NC-ND', b'CC Attribution + Noncommercial + NoDerivatives'), (b'CC BY-NC-SA', b'CC Attribution + Noncommercial + ShareAlike')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='novel',
            name='surl',
            field=models.CharField(unique=True, max_length=16, verbose_name=b'Short URL'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='token',
            name='surl',
            field=models.CharField(unique=True, max_length=16, verbose_name=b'Short URL'),
            preserve_default=True,
        ),
    ]
