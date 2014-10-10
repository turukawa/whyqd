# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Novel'
        db.create_table(u'novel_novel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('surl', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='novel_creator', null=True, to=orm['usr.User'])),
            ('creator_ip', self.gf('django.db.models.fields.GenericIPAddressField')(default='255.255.255.255', max_length=39, null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('license', self.gf('django.db.models.fields.CharField')(default='All Rights Reserved', max_length=50)),
            ('jsonresponse', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
            ('authors', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('authorsort', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('pitch', self.gf('django.db.models.fields.CharField')(max_length=503, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('series', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('series_index', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('ISBN', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('cover_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('sentinal', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='novel_sentinal', unique=True, null=True, to=orm['wiqi.Wiqi'])),
            ('word_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cover_banner', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('cover_thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('ebook_epub', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('ebook_mobi', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('ebook_pdf', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('ebook_azw', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('novel', ['Novel'])

        # Adding M2M table for field chapterlist on 'Novel'
        m2m_table_name = db.shorten_name(u'novel_novel_chapterlist')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('novel', models.ForeignKey(orm['novel.novel'], null=False)),
            ('wiqi', models.ForeignKey(orm['wiqi.wiqi'], null=False))
        ))
        db.create_unique(m2m_table_name, ['novel_id', 'wiqi_id'])

        # Adding model 'Token'
        db.create_table(u'novel_token', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('surl', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='token_creator', null=True, to=orm['usr.User'])),
            ('creator_ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('redeemer', self.gf('django.db.models.fields.related.OneToOneField')(related_name='token_redeemer', unique=True, null=True, to=orm['usr.User'])),
            ('redeemer_ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
            ('redeemed_on', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('novel', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['novel.Novel'], unique=True, null=True, blank=True)),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_purchased', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('recipient', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('novel', ['Token'])


    def backwards(self, orm):
        # Deleting model 'Novel'
        db.delete_table(u'novel_novel')

        # Removing M2M table for field chapterlist on 'Novel'
        db.delete_table(db.shorten_name(u'novel_novel_chapterlist'))

        # Deleting model 'Token'
        db.delete_table(u'novel_token')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'novel.novel': {
            'ISBN': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'Meta': {'object_name': 'Novel'},
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'authorsort': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'chapterlist': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'novel_chapterlist'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['wiqi.Wiqi']"}),
            'cover_banner': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'cover_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'cover_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'novel_creator'", 'null': 'True', 'to': u"orm['usr.User']"}),
            'creator_ip': ('django.db.models.fields.GenericIPAddressField', [], {'default': "'255.255.255.255'", 'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'ebook_azw': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'ebook_epub': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'ebook_mobi': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'ebook_pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jsonresponse': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'default': "'All Rights Reserved'", 'max_length': '50'}),
            'pitch': ('django.db.models.fields.CharField', [], {'max_length': '503', 'blank': 'True'}),
            'sentinal': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'novel_sentinal'", 'unique': 'True', 'null': 'True', 'to': "orm['wiqi.Wiqi']"}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'series_index': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'surl': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'word_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'novel.token': {
            'Meta': {'object_name': 'Token'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'token_creator'", 'null': 'True', 'to': u"orm['usr.User']"}),
            'creator_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_purchased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'novel': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['novel.Novel']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'redeemed_on': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'redeemer': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'token_redeemer'", 'unique': 'True', 'null': 'True', 'to': u"orm['usr.User']"}),
            'redeemer_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'surl': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        u'usr.user': {
            'Meta': {'object_name': 'User'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'blog_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'current_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'current_view': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_open_graph': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_profile_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'new_token_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'website_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'wiqi.wiqi': {
            'Meta': {'object_name': 'Wiqi'},
            'branched_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_wiqi_branched'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'branched_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'branchlist': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'branchlist_rel_+'", 'blank': 'True', 'to': "orm['wiqi.Wiqi']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_live_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'is_live_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_searchable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'merged_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_wiqi_merged'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'merged_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'next_wiqi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_wiqi_next'", 'null': 'True', 'to': "orm['wiqi.Wiqi']"}),
            'previous_wiqi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_wiqi_previous'", 'null': 'True', 'to': "orm['wiqi.Wiqi']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '10', 'decimal_places': '2'}),
            'read_if': ('django.db.models.fields.CharField', [], {'default': "'Open'", 'max_length': '5'}),
            'stack_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_wiqi_base'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'stack_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'surl': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['novel']