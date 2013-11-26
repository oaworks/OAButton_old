# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OAEvent'
        db.create_table(u'bookmarklet_oaevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('coords_lat', self.gf('django.db.models.fields.FloatField')()),
            ('coords_lng', self.gf('django.db.models.fields.FloatField')()),
            ('accessed', self.gf('django.db.models.fields.DateTimeField')()),
            ('doi', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=400)),
            ('story', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('user_slug', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True)),
            ('user_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user_profession', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'bookmarklet', ['OAEvent'])

        # Adding model 'OAUser'
        db.create_table(u'bookmarklet_oauser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('profession', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mailinglist', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
        ))
        db.send_create_signal(u'bookmarklet', ['OAUser'])

        # Adding model 'OASession'
        db.create_table(u'bookmarklet_oasession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('expire', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'bookmarklet', ['OASession'])


    def backwards(self, orm):
        # Deleting model 'OAEvent'
        db.delete_table(u'bookmarklet_oaevent')

        # Deleting model 'OAUser'
        db.delete_table(u'bookmarklet_oauser')

        # Deleting model 'OASession'
        db.delete_table(u'bookmarklet_oasession')


    models = {
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
            'url': ('django.db.models.fields.URLField', [], {'max_length': '400'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        }
    }

    complete_apps = ['bookmarklet']