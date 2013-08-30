"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.sites.models import Site
from django.test.utils import override_settings
from mock import Mock


@override_settings(MONGO_DB=Mock())
class SimpleTest(TestCase):
    def setUp(self):
        current_site = Site.objects.get_current()
        current_site.domain = 'oabutton.com'
        current_site.save()
        self.client = Client()

    def test_bookmarklet(self):
        response = self.client.get('/')
        assert response.context['hostname'] == 'oabutton.com'
        # Do a dumb scan to see that oabutton.com is in the JS url
        bookmarklet_url = response.content.find("('src','http://oabutton.com/static/js/bookmarklet.js')")
        assert bookmarklet_url != -1
