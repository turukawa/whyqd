# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Wiqi'
        db.create_table(u'wiqi_wiqi', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_live_from', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('is_live_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_protected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_searchable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('stack_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wiqi_wiqi_ base', null=True, to=orm['contenttypes.ContentType'])),
            ('stack_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('forked_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wiqi_wiqi_forked', null=True, to=orm['contenttypes.ContentType'])),
            ('forked_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('merged_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wiqi_wiqi_ merged', null=True, to=orm['contenttypes.ContentType'])),
            ('merged_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('next_wiqi', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wiqi_wiqi_ next', null=True, to=orm['wiqi.Wiqi'])),
            ('previous_wiqi', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wiqi_wiqi_ previous', null=True, to=orm['wiqi.Wiqi'])),
        ))
        db.send_create_signal('wiqi', ['Wiqi'])

        # Adding M2M table for field forklist on 'Wiqi'
        m2m_table_name = db.shorten_name(u'wiqi_wiqi_forklist')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_wiqi', models.ForeignKey(orm['wiqi.wiqi'], null=False)),
            ('to_wiqi', models.ForeignKey(orm['wiqi.wiqi'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_wiqi_id', 'to_wiqi_id'])

        # Adding model 'Text'
        db.create_table('text', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usr.User'], null=True)),
            ('creator_ip', self.gf('django.db.models.fields.GenericIPAddressField')(default='255.255.255.255', max_length=39, null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('wiqi', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiqi.Wiqi'], null=True)),
            ('reverted_from_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wiqi_text_ reverted_from', null=True, to=orm['contenttypes.ContentType'])),
            ('reverted_from_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('word_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('header_image_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wiqi_text_ header_image', null=True, to=orm['contenttypes.ContentType'])),
            ('header_image_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal('wiqi', ['Text'])

        # Adding model 'Image'
        db.create_table('image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['usr.User'], null=True)),
            ('creator_ip', self.gf('django.db.models.fields.GenericIPAddressField')(default='255.255.255.255', max_length=39, null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('wiqi', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiqi.Wiqi'], null=True)),
            ('reverted_from_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wiqi_image_ reverted_from', null=True, to=orm['contenttypes.ContentType'])),
            ('reverted_from_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('source_attribution', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('source_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal('wiqi', ['Image'])


    def backwards(self, orm):
        # Deleting model 'Wiqi'
        db.delete_table(u'wiqi_wiqi')

        # Removing M2M table for field forklist on 'Wiqi'
        db.delete_table(db.shorten_name(u'wiqi_wiqi_forklist'))

        # Deleting model 'Text'
        db.delete_table('text')

        # Deleting model 'Image'
        db.delete_table('image')


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
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        },
        u'usr.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_subscribed_to': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'wiqi.image': {
            'Meta': {'ordering': "('created_on',)", 'object_name': 'Image', 'db_table': "'image'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usr.User']", 'null': 'True'}),
            'creator_ip': ('django.db.models.fields.GenericIPAddressField', [], {'default': "'255.255.255.255'", 'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'reverted_from_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_image_ reverted_from'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'reverted_from_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'source_attribution': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'source_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'wiqi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiqi.Wiqi']", 'null': 'True'})
        },
        'wiqi.text': {
            'Meta': {'ordering': "('created_on',)", 'object_name': 'Text', 'db_table': "'text'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['usr.User']", 'null': 'True'}),
            'creator_ip': ('django.db.models.fields.GenericIPAddressField', [], {'default': "'255.255.255.255'", 'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'header_image_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_text_ header_image'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'header_image_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'reverted_from_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_text_ reverted_from'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'reverted_from_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'wiqi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiqi.Wiqi']", 'null': 'True'}),
            'word_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'wiqi.wiqi': {
            'Meta': {'object_name': 'Wiqi'},
            'forked_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_wiqi_forked'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'forked_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'forklist': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'forklist_rel_+'", 'blank': 'True', 'to': "orm['wiqi.Wiqi']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_live_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'is_live_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_searchable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'merged_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_wiqi_ merged'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'merged_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'next_wiqi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_wiqi_ next'", 'null': 'True', 'to': "orm['wiqi.Wiqi']"}),
            'previous_wiqi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_wiqi_ previous'", 'null': 'True', 'to': "orm['wiqi.Wiqi']"}),
            'stack_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wiqi_wiqi_ base'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'stack_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['wiqi']