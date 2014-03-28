# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OABlockedURL'
        db.create_table(u'bookmarklet_oablockedurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True)),
            ('author_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('blocked_url', self.gf('django.db.models.fields.URLField')(max_length=2000, db_index=True)),
            ('open_url', self.gf('django.db.models.fields.URLField')(max_length=2000, db_index=True)),
        ))
        db.send_create_signal(u'bookmarklet', ['OABlockedURL'])

        # Adding index on 'OAEvent', fields ['url']
        db.create_index(u'bookmarklet_oaevent', ['url'])


    def backwards(self, orm):
        # Removing index on 'OAEvent', fields ['url']
        db.delete_index(u'bookmarklet_oaevent', ['url'])

        # Deleting model 'OABlockedURL'
        db.delete_table(u'bookmarklet_oablockedurl')


    models = {
        u'bookmarklet.oablockedurl': {
            'Meta': {'object_name': 'OABlockedURL'},
            'author_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'blocked_url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'})
        },
        u'bookmarklet.oaevent': {
            'Meta': {'object_name': 'OAEvent'},
            'accessed': ('django.db.models.fields.DateTimeField', [], {}),
            'coords_lat': ('django.db.models.fields.FloatField', [], {}),
            'coords_lng': ('django.db.models.fields.FloatField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'doi': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'story': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'db_index': 'True'}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_profession': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_slug': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'})
        },
        u'bookmarklet.oasession': {
            'Meta': {'object_name': 'OASession'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'expire': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'bookmarklet.oauser': {
            'Meta': {'object_name': 'OAUser'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            'email_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        }
    }

    complete_apps = ['bookmarklet']