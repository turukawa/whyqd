# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('about_me', models.TextField(null=True, blank=True)),
                ('facebook_id', models.BigIntegerField(unique=True, null=True, blank=True)),
                ('access_token', models.TextField(help_text='Facebook token for offline access', null=True, blank=True)),
                ('facebook_name', models.CharField(max_length=255, null=True, blank=True)),
                ('facebook_profile_url', models.TextField(null=True, blank=True)),
                ('website_url', models.TextField(null=True, blank=True)),
                ('blog_url', models.TextField(null=True, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True, choices=[('m', 'Male'), ('f', 'Female')])),
                ('raw_data', models.TextField(null=True, blank=True)),
                ('facebook_open_graph', models.NullBooleanField(help_text='Determines if this user want to share via open graph')),
                ('new_token_required', models.BooleanField(default=False, help_text='Set to true if the access token is outdated or lacks permissions')),
                ('image', models.ImageField(max_length=255, null=True, upload_to='images\\facebook_profiles/%Y/%m/%d', blank=True)),
                ('current_view', models.CharField(max_length=32, verbose_name=b'Current chapter view.', blank=True)),
                ('current_price', models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
    ]
