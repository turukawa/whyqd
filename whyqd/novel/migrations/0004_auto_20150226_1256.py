# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0003_novel_show_charge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='novel',
            old_name='show_charge',
            new_name='show_buy',
        ),
    ]
