"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from oabutton.apps.bookmarklet.models import Event
import json
from oabutton.json_util import MyEncoder

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
