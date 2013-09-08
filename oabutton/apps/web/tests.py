"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from mock import MagicMock


@override_settings(HOSTNAME='localhost:8000')
class SimpleTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_bookmarklet(self):
        response = self.client.get('/')
        assert response.context['hostname'] == 'localhost:8000'
        # Do a dumb scan to see that oabutton.com is in the JS url
        bookmarklet_url = response.content.find(
                "('src','http://localhost:8000/static/js/bookmarklet.js')")
        assert bookmarklet_url != -1

    def test_count_denied_pursuits(self):
        raise NotImplementedError
        response = self.client.get('/')
        assert response.context['count'] == 2
        assert response.content.find("<h1>2<small> Scholarly pursuits") != -1
