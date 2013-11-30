"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from mock import MagicMock, patch
from nose.tools import eq_, ok_
from oabutton.apps.bookmarklet.models import OAEvent
import BeautifulSoup

# TODO: tests should probably use real database data as the views
# actually load from disk and render to JSON. Remove these mocks.

# This sets up a mock for the OAEvent class
all_objs = MagicMock()
all_objs.to_json.return_value = [MagicMock(), MagicMock()]
MockOAEvent = MagicMock(wraps=OAEvent)
MockOAEvent.objects.count.return_value = 2
MockOAEvent.objects.all.return_value = all_objs


class SimpleTest(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('oabutton.apps.bookmarklet.models.OAEvent', MockOAEvent)
    def test_count_denied_pursuits(self):
        response = self.client.get('/')
        eq_(response.context['count'], 2)

        soup = BeautifulSoup.BeautifulSoup(response.content)
        node = soup.find('span', attrs={'id': 'counter'})
        eq_(node.text, '2')
        eq_(node.nextSibling.text, u'Paywalls Hit')

    @patch('oabutton.apps.bookmarklet.models.OAEvent', MockOAEvent)
    def test_versioned_static_content(self):
        response = self.client.get('/')
        soup = BeautifulSoup.BeautifulSoup(response.content)
        scripts = [s for s in soup.findAll('script')
                   if s.get('src', '').startswith("/static")]
        sheets = soup.findAll('link', attrs={'rel': 'stylesheet'})

        ok_(len(scripts) > 0)
        ok_(len(sheets) > 0)

        v = settings.VERSION
        for s in scripts:
            version_check = s['src'].endswith(".js?version=%s" % v)
            ok_(version_check)

        for s in sheets:
            ok_(s['href'].endswith(".css?version=%s" % v))
