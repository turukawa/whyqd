# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import whyqd.novel.models.novels
import jsonfield.fields
from decimal import Decimal
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wiqi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surl', models.CharField(unique=True, max_length=16, verbose_name=b'Short URL')),
                ('title', models.CharField(help_text=b'This may be used as a title, section or figure heading.', max_length=250, verbose_name=b'Title', blank=True)),
                ('creator_ip', models.GenericIPAddressField(default=b'255.255.255.255', null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('licensing', models.CharField(default=b'(c)', help_text=b'What form of copyright do you offer?', max_length=50, verbose_name=b'Release License', choices=[(b'(c)', b'All Rights Reserved'), (b'CC0', b'No Rights Reserved'), (b'CC BY', b'CC Attribution'), (b'CC BY-ND', b'CC Attribution + NoDerivatives'), (b'CC BY-SA', b'CC Attribution + ShareAlike'), (b'CC BY-NC', b'CC Attribution + Noncommercial'), (b'CC BY-NC-ND', b'CC Attribution + Noncommercial + NoDerivatives'), (b'CC BY-NC-SA', b'CC Attribution + Noncommercial + ShareAlike')])),
                ('jsonresponse', jsonfield.fields.JSONField(null=True, blank=True)),
                ('authors', models.CharField(help_text=b'Comma-separated list of all authors.', max_length=250, verbose_name=b'Author names', blank=True)),
                ('authorsort', models.CharField(help_text=b"Author list by 'surname, name'; for listing.", max_length=250, verbose_name=b'Sortable author list', blank=True)),
                ('pitch', models.CharField(help_text=b'You have 503 characters. Sell it to me.', max_length=503, verbose_name=b'Elevator Pitch', blank=True)),
                ('summary', models.TextField(help_text=b'The back cover of your book.', verbose_name=b'Summary', blank=True)),
                ('language', models.CharField(help_text=b"The language you're writing in.", max_length=50, verbose_name=b'Published language', blank=True)),
                ('series', models.CharField(help_text=b'Is the book part of a series?', max_length=150, verbose_name=b'Book series', blank=True)),
                ('series_index', models.CharField(help_text=b'What number in the series?', max_length=10, verbose_name=b'Series index', blank=True)),
                ('ISBN', models.CharField(help_text=b'Enter the 13-digit ISBN for your book. Can include dashes or spaces.', max_length=40, verbose_name=b'13-digit ISBN for your book.', blank=True)),
                ('cover_image', models.ImageField(upload_to=whyqd.novel.models.novels.get_covername, blank=True)),
                ('chapterformat', jsonfield.fields.JSONField(null=True, blank=True)),
                ('word_count', models.IntegerField(null=True, blank=True)),
                ('cover_banner', models.ImageField(upload_to=whyqd.novel.models.novels.get_covername, blank=True)),
                ('cover_thumbnail', models.ImageField(upload_to=whyqd.novel.models.novels.get_covername, blank=True)),
                ('ebook_epub', models.FileField(upload_to=whyqd.novel.models.novels.get_ebookname, blank=True)),
                ('ebook_mobi', models.FileField(upload_to=whyqd.novel.models.novels.get_ebookname, blank=True)),
                ('ebook_pdf', models.FileField(upload_to=whyqd.novel.models.novels.get_ebookname, blank=True)),
                ('ebook_azw', models.FileField(upload_to=whyqd.novel.models.novels.get_ebookname, blank=True)),
                ('defaultcurrency', models.CharField(default=b'gbp', max_length=7, choices=[(b'gbp', b'&pound;'), (b'usd', b'$'), (b'eur', b'&euro;')])),
                ('defaultprice', models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2)),
                ('discountvolume', models.IntegerField(null=True, blank=True)),
                ('discountpercent', models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2)),
                ('lendnumber', models.IntegerField(null=True, blank=True)),
                ('lenddays', models.IntegerField(null=True, blank=True)),
                ('chapterlist', models.ManyToManyField(related_name='novel_chapterlist', null=True, to='wiqi.Wiqi', blank=True)),
                ('creator', models.ForeignKey(related_name='novel_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('sentinal', models.OneToOneField(related_name='novel_sentinal', null=True, blank=True, to='wiqi.Wiqi')),
            ],
            options={
                'verbose_name_plural': 'Novels',
                'permissions': (('can_create', 'Can create new novels.'), ('can_view', 'Can view private novel.'), ('can_edit', 'Can edit novel.'), ('can_publish', 'Can change publication status of novel.'), ('can_share', 'Can share access of novel with others.'), ('owns', 'Has purchased the object.'), ('borrowed', 'Has borrowed the object.')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surl', models.CharField(unique=True, max_length=25, verbose_name=b'Short URL')),
                ('creator_ip', models.GenericIPAddressField(null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('redeemer_ip', models.GenericIPAddressField(null=True, blank=True)),
                ('redeemed_on', models.DateTimeField(null=True, blank=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('is_purchased', models.BooleanField(default=False)),
                ('charge', jsonfield.fields.JSONField(null=True, blank=True)),
                ('currency', models.CharField(default=b'gbp', max_length=7, choices=[(b'gbp', b'&pound;'), (b'usd', b'$'), (b'eur', b'&euro;')])),
                ('price', models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2)),
                ('recipient', models.EmailField(max_length=75, null=True, verbose_name=b'Email', blank=True)),
                ('creator', models.ForeignKey(related_name='token_creator', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('novel', models.ForeignKey(blank=True, to='novel.Novel', null=True)),
                ('redeemer', models.ForeignKey(related_name='token_redeemer', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Tokens',
            },
            bases=(models.Model,),
        ),
    ]
