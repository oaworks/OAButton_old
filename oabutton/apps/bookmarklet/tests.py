"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from nose.tools import eq_, ok_
from oabutton.apps.bookmarklet.models import OAEvent, OAUser, OASession
import dateutil.parser
import json
import re


class APITest(TestCase):
    def setUp(self):
        """
        verify that the JSON emitted is compatible with the javascript
        map stuff
        """
        # check that we have all the signin fields
        self.EMAIL = 'new_email@foo.com'
        self.POST_DATA = {u'email': self.EMAIL,
                          'name': 'some name',
                          'profession': 'Student',
                          'confirm_public': 'checked',
                          'mailinglist': 'checked'}

        for user in OAUser.objects.filter(email=self.EMAIL):
            user.delete()

        c = Client()
        response = c.post('/api/signin/', self.POST_DATA)

        eq_(response.status_code, 200)
        self.user = OAUser.objects.get(email=self.EMAIL)

        eq_(self.user.name, 'some name')
        eq_(self.user.email, self.EMAIL)
        eq_(self.user.profession, 'Student')
        ok_(self.user.mailinglist)

        # Check that a confirmation email went out
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        assert msg.to == [self.user.email]
        url = self.user.get_confirm_path()
        assert url in msg.body
        mail.outbox = []

    def test_add_post(self):
        '''
        We need to make sure all fields of the OAEvent object are
        serialized back to MongoDB
        '''
        POST_DATA = {u'story': [u'some access requirement'],
                     u'doi': [u'10.1016/j.urology.2010.05.009.'],
                     u'url': [u'http://www.ncbi.nlm.nih.gov/pubmed/20709373'],
                     u'coords': [u'44,-79.5'],
                     u'location': [u'Somewhere'],
                     u'accessed': [u'Mon, 09 Sep 2013 14:54:42 GMT'],
                     u'description': [u'some description'],
                     u'slug': self.user.slug, }

        c = Client()
        response = c.get('/api/form/page1/%s/' % self.user.slug)
        key = response.context['key']
        response = c.post('/api/post/%s/' % key, POST_DATA)
        assert response.status_code == 302

        s = OASession.objects.get(key=key)
        data = json.loads(s.data)
        evt = OAEvent.objects.get(id=data['event_id'])

        expected = {'doi': u'10.1016/j.urology.2010.05.009.',
                    'url': u'http://www.ncbi.nlm.nih.gov/pubmed/20709373',
                    'coords': {u'lat': 44.0, u'lng': -79.5},
                    'location': 'Somewhere',
                    'accessed': dateutil.parser.parse(POST_DATA['accessed'][0]),
                    'user_email': self.EMAIL}
        for k, v in expected.items():
            eq_(getattr(evt, k), v)

    def test_add_post_no_latlong(self):
        '''
        We need to make sure all fields of the OAEvent object are
        serialized back to MongoDB
        '''
        POST_DATA = {u'story': [u'some access requirement'],
                     u'doi': [u'10.1016/j.urology.2010.05.009.'],
                     u'url': [u'http://www.ncbi.nlm.nih.gov/pubmed/20709373'],
                     u'coords': [u''],
                     u'location': [u'Somewhere'],
                     u'accessed': [u'Mon, 09 Sep 2013 14:54:42 GMT'],
                     u'description': [u'some description'],
                     u'slug': self.user.slug, }

        c = Client()
        response = c.get('/api/form/page1/%s/' % self.user.slug)
        key = response.context['key']
        response = c.post('/api/post/%s/' % key, POST_DATA)

        assert response.status_code == 302

        s = OASession.objects.get(key=key)
        data = json.loads(s.data)
        evt = OAEvent.objects.get(id=data['event_id'])

        expected = {'doi': u'10.1016/j.urology.2010.05.009.',
                    'url': u'http://www.ncbi.nlm.nih.gov/pubmed/20709373',
                    'coords': {u'lat': 0.0, u'lng': 0},
                    'location': 'Somewhere',
                    'accessed': dateutil.parser.parse(POST_DATA['accessed'][0]),
                    'user_email': self.EMAIL}
        for k, v in expected.items():
            eq_(getattr(evt, k), v)

    def test_event_json(self):
        """
        verify that the JSON emitted is compatible with the javascript
        map stuff
        """
        user = self.user

        POST_DATA = {u'story': [u'some access requirement'],
                     u'doi': [u'10.1016/j.urology.2010.05.009.'],
                     u'url': [u'http://www.ncbi.nlm.nih.gov/pubmed/20709373'],
                     u'coords': [u'44,-79.5'],
                     u'location': [u''],
                     u'accessed': [u'Mon, 09 Sep 2013 14:54:42 GMT'],
                     u'description': [u'some description'],
                     u'slug': user.slug}

        c = Client()
        response = c.get('/api/form/page1/%s/' % self.user.slug)
        key = response.context['key']
        response = c.post('/api/post/%s/' % key, POST_DATA)
        assert response.status_code == 302

        s = OASession.objects.get(key=key)
        data = json.loads(s.data)

        evt = OAEvent.objects.get(id=data['event_id'])
        eq_(evt.coords, {'lat': 44.0, 'lng': -79.5})
        eq_(evt.doi, '10.1016/j.urology.2010.05.009.')
        eq_(evt.url, 'http://www.ncbi.nlm.nih.gov/pubmed/20709373')

        actual_date = evt.accessed
        eq_(actual_date.year, 2013)
        eq_(actual_date.month, 9)
        eq_(actual_date.day, 9)

        eq_(evt.user_name, 'some name')
        eq_(evt.user_profession, 'Student')
        eq_(evt.story, 'some access requirement')

        # Check that we can resolve the original user oid
        evt = OAEvent.objects.filter(id=data['event_id'])[0]
        assert evt.user_slug is not None

    def test_update_signon(self):
        # Update doesn't anymore. We just create new users.
        """
        verify that the JSON emitted is compatible with the javascript
        map stuff
        """
        user = self.user

        c = Client()
        response = c.post('/api/signin/', self.POST_DATA)

        eq_(response.status_code, 200)
        # Extract the slug frmo the javascript URL
        new_slug = json.loads(response.content)['url'][-35:-3]

        # check that we have all the signin fields
        user = OAUser.objects.get(slug=new_slug)
        eq_(user.name, 'some name')
        eq_(user.email, self.EMAIL)
        eq_(user.profession, 'Student')
        ok_(user.mailinglist)

    def test_search_doi_after_post(self):
        '''
        Tests to make sure the response to submitting the form is rendered
        correctly.
        '''
        POST_DATA = {'name': 'mock name',
                     'profession': 'mock profession',
                     'location': 'mock location',
                     'coords': '33.2,21.9',
                     'accessed': 'Mon, 09 Sep 2013 14:54:42 GMT',
                     'doi': 'some.doi',
                     'url': 'http://some.url/some_path',
                     'story': 'some_story',
                     'email': 'foo@blah.com',
                     'slug': self.user.slug,
                     }

        c = Client()
        response = c.get('/api/form/page1/%s/' % self.user.slug)
        key = response.context['key']
        slug = response.context['slug']

        response = c.post('/api/post/%s/' % key, POST_DATA)
        assert response.status_code == 302

        response = c.get(reverse('bookmarklet:form2', kwargs={'key': key, 'slug': slug}))
        assert response.status_code == 200

        response = c.post(reverse('bookmarklet:form3', kwargs={'key': key, 'slug': slug}), POST_DATA)
        # Check that the DOI is passed through correctly
        data_doi_re = re.compile('<body [^>]*data-doi="%s">'
                                 % POST_DATA['doi'])
        assert data_doi_re.search(response.content) is not None

    def test_confirmation_email(self):
        self.user.send_confirmation_email()
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]

        url = self.user.get_confirm_path()

        assert msg.to == [self.user.email]
        assert url in msg.body

        # click the verification link
        c = Client()
        response = c.get(url)
        eq_(response.status_code, 200)
        # Reload the user as it's been changed
        self.user = OAUser.objects.get(email=self.EMAIL)
        assert self.user.email_confirmed

    def test_confirmation_email_fail(self):
        self.user.send_confirmation_email()
        self.assertEqual(len(mail.outbox), 1)

        url = self.user.get_confirm_path()
        url = url.replace("_", "_1234")

        # click the wrong verification link
        c = Client()
        response = c.get(url)
        eq_(response.status_code, 200)
        # Reload the user as it's been changed
        self.user = OAUser.objects.get(email=self.EMAIL)
        assert self.user.email_confirmed is False
