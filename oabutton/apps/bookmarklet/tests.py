"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from nose.tools import eq_, ok_
from oabutton.apps.bookmarklet.models import Event, User
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
                     u'url': [u'http://www.ncbi.nlm.nih.gov/pubmed/20709373'],
                     u'coords': [u'44,-79.5'],
                     u'location': [u'Somewhere'],
                     u'accessed': [u'Mon, 09 Sep 2013 14:54:42 GMT'],
                     u'description': [u'some description']}

        c = Client()
        response = c.post('/api/post/', POST_DATA)

        assert response.status_code == 200

        evt = Event.objects.get(id=response.context['oid'])

        expected = {'doi': u'10.1016/j.urology.2010.05.009.',
                    'url': u'http://www.ncbi.nlm.nih.gov/pubmed/20709373',
                    'coords': {u'lat': 44.0, u'lng': -79.5},
                    'location': 'Somewhere',
                    'accessed': datetime.datetime(2013, 9, 9, 14, 54, 42),
                    'pub_date': None,
                    'email': None}
        for k, v in expected.items():
            assert getattr(evt, k) == v

    def test_event_json(self):
        """
        verify that the JSON emitted is compatible with the javascript
        map stuff
        """

        POST_DATA = {u'story': [u'some access requirement'],
                     u'doi': [u'10.1016/j.urology.2010.05.009.'],
                     u'url': [u'http://www.ncbi.nlm.nih.gov/pubmed/20709373'],
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

    def test_new_signon(self):
        """
        verify that the JSON emitted is compatible with the javascript
        map stuff
        """

        EMAIL = 'new_email@foo.com'
        POST_DATA = {u'email': [EMAIL],
                'privacy': 'PUBLIC'}

        for user in User.objects.filter(username=EMAIL):
            user.delete()

        c = Client()
        response = c.post('/api/signin/', POST_DATA)

        eq_(response.status_code, 200)
        ok_('url' in json.loads(response.content))

    def test_update_signon(self):
        """
        verify that the JSON emitted is compatible with the javascript
        map stuff
        """

        EMAIL = 'new_email@foo.com'
        POST_DATA = {u'email': [EMAIL],
                'privacy': 'PUBLIC'}

        for user in User.objects.filter(username=EMAIL):
            user.delete()
        from django.contrib.auth import get_user_model
        manager = get_user_model()._default_manager

        user = manager.create_user(email=EMAIL, username=EMAIL, privacy='PUBLIC')

        c = Client()
        response = c.post('/api/signin/', POST_DATA)

        eq_(response.status_code, 200)
        eq_({'url': user.get_bookmarklet_url()}, json.loads(response.content))
