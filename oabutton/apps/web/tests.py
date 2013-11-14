"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from mock import MagicMock, patch
from nose.tools import eq_, ok_
from oabutton.apps.bookmarklet.models import Event
import re

# This sets up a mock for the Event class
all_objs = MagicMock()
all_objs.to_json.return_value = [MagicMock(), MagicMock()]
MockEvent = MagicMock(wraps=Event)
MockEvent.objects.count.return_value = 2
MockEvent.objects.all.return_value = all_objs


class SimpleTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_bookmarklet(self):
        response = self.client.get('/')
        eq_(response.context['hostname'], 'http://localhost:8000')
        # Do a dumb scan to see that oabutton.com is in the JS url
        # TODO: bring back this test when the Jade templates have been
        # finalized
        #bookmarklet_url = response.content.find("('src', 'http://localhost:8000/static/js/bookmarklet.js')")
        #ok_(bookmarklet_url != -1)

    @patch('oabutton.apps.bookmarklet.models.Event', MockEvent)
    def test_count_denied_pursuits(self):
        response = self.client.get('/')
        eq_(response.context['count'], 2)

        content = re.sub(r'\s+', ' ', response.content)
        ok_(content.find(r"""<span id="counter">2 </span><span>Paywalls Hit </span>""") != -1)
