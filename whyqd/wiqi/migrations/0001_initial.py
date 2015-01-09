# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from decimal import Decimal
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surl', models.CharField(max_length=32, verbose_name=b'Short URL', blank=True)),
                ('title', models.CharField(help_text=b'This may be used as a title, section or figure heading.', max_length=250, verbose_name=b'Title', blank=True)),
                ('description', models.TextField(help_text=b'May only be necessary where the content may not provide sufficient context.', verbose_name=b'Description', blank=True)),
                ('creator_ip', models.GenericIPAddressField(default=b'255.255.255.255', null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('license', models.CharField(default=b'All Rights Reserved', help_text=b'What form of copyright do you offer?', max_length=50, verbose_name=b'Release License', choices=[(b'(c)', b'All Rights Reserved'), (b'CC0', b'No Rights Reserved'), (b'CC BY', b'CC Attribution'), (b'CC BY-ND', b'CC Attribution + NoDerivatives'), (b'CC BY-SA', b'CC Attribution + ShareAlike'), (b'CC BY-NC', b'CC Attribution + Noncommercial'), (b'CC BY-NC-ND', b'CC Attribution + Noncommercial + NoDerivatives'), (b'CC BY-NC-SA', b'CC Attribution + Noncommercial + ShareAlike')])),
                ('citation', models.CharField(default=b'', help_text=b"Please reference the original creator, if it wasn't you.", max_length=150, blank=True)),
                ('jsonresponse', jsonfield.fields.JSONField(null=True, blank=True)),
                ('reverted_from_object_id', models.PositiveIntegerField(null=True)),
                ('subtitle', models.CharField(help_text=b'An elaboration of the title.', max_length=500, verbose_name=b'Subtitle', blank=True)),
                ('content', models.TextField(help_text=b'Use html format to enter text.', verbose_name=b'Content', blank=True)),
                ('word_count', models.IntegerField(null=True, blank=True)),
                ('creator', models.ForeignKey(related_name='wiqi_text_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('reverted_from_content_type', models.ForeignKey(related_name='wiqi_text_reverted_from', to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('created_on',),
                'abstract': False,
                'db_table': 'text',
                'verbose_name_plural': 'Texts',
                'get_latest_by': 'created_on',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wiqi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surl', models.CharField(max_length=32, verbose_name=b'Short URL', blank=True)),
                ('is_live_from', models.DateTimeField(default=datetime.datetime.now, help_text=b'Leave blank to publish immediately, otherwise select a future publication date.', null=True, verbose_name=b'Publish from', blank=True)),
                ('is_live_to', models.DateTimeField(help_text=b'Leave blank for permanent publication, otherwise select a date to end publication.', null=True, verbose_name=b'Publish until', blank=True)),
                ('is_private', models.BooleanField(default=False, help_text=b'If unselected, the wiqi will be public.', verbose_name=b'Private')),
                ('is_active', models.BooleanField(default=True)),
                ('is_searchable', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('stack_object_id', models.PositiveIntegerField(null=True)),
                ('branched_object_id', models.PositiveIntegerField(null=True)),
                ('merged_object_id', models.PositiveIntegerField(null=True)),
                ('read_if', models.CharField(default=b'Open', max_length=5, choices=[(b'open', b'Open'), (b'login', b'Login'), (b'own', b'Own')])),
                ('price', models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2)),
                ('branched_content_type', models.ForeignKey(related_name='wiqi_wiqi_branched', to='contenttypes.ContentType', null=True)),
                ('branchlist', models.ManyToManyField(related_name='branchlist_rel_+', to='wiqi.Wiqi', blank=True)),
                ('merged_content_type', models.ForeignKey(related_name='wiqi_wiqi_merged', to='contenttypes.ContentType', null=True)),
                ('next_wiqi', models.ForeignKey(related_name='wiqi_wiqi_next', to='wiqi.Wiqi', null=True)),
                ('previous_wiqi', models.ForeignKey(related_name='wiqi_wiqi_previous', to='wiqi.Wiqi', null=True)),
                ('stack_content_type', models.ForeignKey(related_name='wiqi_wiqi_base', to='contenttypes.ContentType', null=True)),
            ],
            options={
                'permissions': (('can_create', 'Can create new documents.'), ('can_view', 'Can view private object.'), ('can_view_stack', 'Can view history of private object.'), ('can_edit', 'Can edit private object and its history.'), ('can_publish', 'Can change publication status of private object.'), ('can_change_privacy', 'Can change object privacy.'), ('can_revert', 'Can revert live object from historical object.'), ('can_branch', 'Can branch the object to a new wiqi.'), ('can_merge', 'Can merge the object into an existing wiqi.'), ('owns', 'Has purchased the object.'), ('borrowed', 'Has borrowed the object.'), ('can_share_view', 'Can share access of private object with others.'), ('can_share_view_stack', 'Can share access of view history.'), ('can_share_edit', 'Can share access of edit private object.'), ('can_share_publish', 'Can share access of change publication status.'), ('can_share_privacy', 'Can share access of change object privacy.'), ('can_share_revert', 'Can share access of revert live object.'), ('can_share_branch', 'Can share access of branch to a new wiqi.'), ('can_share_merge', 'Can share access of merge into an existing wiqi.')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='text',
            name='wiqi',
            field=models.ForeignKey(to='wiqi.Wiqi', null=True),
            preserve_default=True,
        ),
    ]
