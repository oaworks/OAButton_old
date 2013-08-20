"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from oabutton.apps.bookmarklet.models import Event


class SimpleTest(TestCase):

    def test_events_to_json(self):
        event = Event()
        event.coords = "44,-22.45"
        event.save()
        jdata = event.to_json()
        new_event = Event()
        new_event.from_json(jdata)
        assert event.id == new_event.id
        assert event.coords == new_event.coords
        pass

    def test_stories(self):
        # TODO: add a test to make sure we're grabbing only the last
        # 50 stories in reverse chronological order
        pass
