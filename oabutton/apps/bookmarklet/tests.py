"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from nose.tools import eq_, ok_
from oabutton.apps.bookmarklet.models import Event
from test_mongoauth import MongoAuthTest
import datetime
import json

class APITest(TestCase):
    def test_add_post(self):
        '''
        We need to make sure all fields of the Event object are
        serialized back to MongoDB
        '''
        POST_DATA = {u'story': [u'some access requirement'],
        u'doi': [u'10.1016/j.urology.2010.05.009.'],
        u'name': [u'Victor Ng'],
        u'url': [u'http://www.ncbi.nlm.nih.gov/pubmed/20709373'],
        u'remember': [u'on'],
        u'profession': [u'engineer'],
        u'coords': [u'44,-79.5'],
        u'location': [u''],
        u'accessed': [u'Mon, 09 Sep 2013 14:54:42 GMT'],
        u'description': [u'some description']}

        c = Client()
        response = c.post('/api/post/', POST_DATA)

        assert response.status_code == 200

        evt = Event.objects.get(id=response.context['oid'])

        expected = {
        'doi': u'10.1016/j.urology.2010.05.009.', 
        'name': u'Victor Ng', 
        'url': u'http://www.ncbi.nlm.nih.gov/pubmed/20709373',
        'profession': u'engineer', 
        'coords': {u'lat': 44.0, u'lng': -79.5}, 
        'location': None,
        'accessed': datetime.datetime(2013, 9, 9, 14, 54, 42),
        'pub_date': None, 
        'email': None}
        for k, v in expected.items():
            assert getattr(evt, k) == v

    def test_event_json(self):

        POST_DATA = {u'story': [u'some access requirement'],
        u'doi': [u'10.1016/j.urology.2010.05.009.'],
        u'name': [u'Victor Ng'],
        u'url': [u'http://www.ncbi.nlm.nih.gov/pubmed/20709373'],
        u'remember': [u'on'],
        u'profession': [u'engineer'],
        u'coords': [u'44,-79.5'],
        u'location': [u''],
        u'accessed': [u'Mon, 09 Sep 2013 14:54:42 GMT'],
        u'description': [u'some description']}

        c = Client()
        response = c.post('/api/post/', POST_DATA)

        assert response.status_code == 200

        json_data = Event.objects.filter(id=response.context['oid']).to_json()
        jdata = json.loads(json_data)
        eq_(len(jdata), 1)
        eq_(jdata[0]['coords'], {'lat': 44.0, 'lng': -79.5})
        eq_(jdata[0]['doi'], '10.1016/j.urology.2010.05.009.')
        eq_(jdata[0]['url'], 'http://www.ncbi.nlm.nih.gov/pubmed/20709373')

