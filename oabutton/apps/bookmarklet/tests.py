"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from mock import MagicMock
from oabutton.apps.bookmarklet.models import Event
from oabutton.apps.bookmarklet.views import convert_post
from oabutton.json_util import MyEncoder
import json


@override_settings(MONGO_DB=MagicMock())
class SimpleTest(TestCase):

    def test_events_to_dict(self):
        event = Event()
        event.coords = {'lat': 44, 'lng': -22.45}
        event.save()
        jdata = json.dumps(event.to_dict(), cls=MyEncoder)
        new_event = Event()
        new_event.from_json(jdata)
        assert event.id == new_event.id
        assert event.coords == new_event.coords

    def test_stories(self):
        # TODO: add a test to make sure we're grabbing only the last
        # 50 stories in reverse chronological order
        pass

    def test_add_post(self):
        '''
        We need to make sure all fields of the Event object are
        serialized back to MongoDB
        '''
        POST_DATA = {'name': 'mock name',
                     'profession': 'mock profession',
                     'location': 'mock location',
                     'coords': '33.2,21.9',
                     'accessed': '2013-09-07T04:21:02.407511',
                     'pub_date': '2013-10-07T04:21:02.407511',
                     'doi': 'some.doi',
                     'url': 'http://some.url/some_path',
                     'story': 'some_story',
                     'email': 'foo@blah.com'}

        c = Client()
        response = c.post('/api/post/', POST_DATA)

        assert response.status_code == 200

        from django.conf import settings
        db = settings.MONGO_DB()

        event = Event()
        convert_post(POST_DATA, event)

        MONGO_DATA = event.to_dict()
        db.events.insert.assert_called_with(MONGO_DATA)

        # Verify that all keys are at least in the MONGO_DATA
        for k in POST_DATA:
            assert k in MONGO_DATA
        assert MONGO_DATA['coords'] == {'lat': '33.2', 'lng': '21.9'}
