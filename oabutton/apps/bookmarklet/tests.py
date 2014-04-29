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
import dateutil.parser
import json
import re

import mock

from oabutton.apps.bookmarklet.email_tools import send_author_notification
from oabutton.apps.bookmarklet.models import OAEvent, OAUser, OASession
from oabutton.apps.bookmarklet.models import OABlockedURL
from oabutton.apps.bookmarklet.models import best_open_url


MOCK_URL = "http://this.is.mocked.by.mock/foo/"


class MockGET(object):
    def __init__(self, status_code):
        self.status_code = status_code


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
        serialized back to db
        '''
        POST_DATA = {u'story': [u'some access requirement'],
                     u'doi': [u'10.1016/j.urology.2010.05.009.'],
                     u'url': [MOCK_URL],
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
                    'url': MOCK_URL,
                    'coords': {u'lat': 44.0, u'lng': -79.5},
                    'location': 'Somewhere',
                    'accessed': dateutil.parser.parse(POST_DATA['accessed'][0]),
                    'user_email': self.EMAIL}
        for k, v in expected.items():
            eq_(getattr(evt, k), v)

    def test_add_post_no_latlong(self):
        '''
        We need to make sure all fields of the OAEvent object are
        serialized back to db
        '''
        POST_DATA = {u'story': [u'some access requirement'],
                     u'doi': [u'10.1016/j.urology.2010.05.009.'],
                     u'url': [MOCK_URL],
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
                    'url': MOCK_URL,
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
                     u'url': [MOCK_URL],
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
        eq_(evt.url, MOCK_URL)

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
        # Extract the slug from the javascript URL
        new_slug = json.loads(response.content)['url'][-35:-3]

        # check that we have all the signin fields
        user = OAUser.objects.get(slug=new_slug)
        eq_(user.name, 'some name')
        eq_(user.email, self.EMAIL)
        eq_(user.profession, 'Student')
        ok_(user.mailinglist)

    @mock.patch('oabutton.phantomjs.email_extractor.scrape_email', mock.Mock(return_value=('mock@mock.com',)))
    @mock.patch('requests.get', mock.Mock(side_effect=[MockGET(200)]))
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
                     'url': MOCK_URL,
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

    def test_notify_author(self):
        """
        On creating an OAEvent record, we need to scan to see if this
        is a new URL.

        If it is, scan for an email address, and try to notify the
        author of the paywall block.
        """
        author_email, blocked_url = 'test@test.com', MOCK_URL
        send_author_notification(author_email, blocked_url)
        blocked = list(OABlockedURL.objects.all())
        slug = blocked[0].slug
        url = reverse('bookmarklet:open_document', kwargs={'slug': slug})

        # Check that a confirmation email went out
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        assert msg.to == [author_email]
        assert url in msg.body
        mail.outbox = []

    @mock.patch('requests.get', mock.Mock(side_effect=[MockGET(404)]))
    def test_add_oa_document_404(self):
        '''
        Add a link to an open access version of the document
        '''
        # First send the author an email notification
        author_email, blocked_url = 'test@test.com', 'http://test.com/some/url/'
        open_url = 'http://some.open.com/some/url/'
        send_author_notification(author_email, blocked_url)

        blocked = list(OABlockedURL.objects.all())
        obj = blocked[0]
        slug = obj.slug
        c = Client()
        response = c.get(reverse('bookmarklet:open_document', kwargs={'slug': slug}))
        eq_(response.status_code, 200)

        assert author_email in response.content
        assert blocked_url in response.content

        post_data = {'author_email': author_email,
                     'blocked_url': blocked_url,
                     'open_url': open_url,
                     'slug': slug}

        response = c.post(reverse('bookmarklet:open_document', kwargs={'slug': slug}), post_data)
        eq_(response.status_code, 200)
        obj = OABlockedURL.objects.get(id=obj.id)
        eq_(obj.open_url, "")
        self.assertTrue("The link you submitted was not reachable" in response.content)

    @mock.patch('requests.get', mock.Mock(side_effect=[MockGET(200)]))
    def test_add_oa_document_200(self):
        '''
        Add a link to an open access version of the document
        '''
        # First send the author an email notification
        author_email, blocked_url = 'test@test.com', 'http://test.com/some/url/'
        open_url = 'http://some.open.com/some/url/'
        send_author_notification(author_email, blocked_url)

        blocked = list(OABlockedURL.objects.all())
        obj = blocked[0]
        slug = obj.slug
        c = Client()
        response = c.get(reverse('bookmarklet:open_document', kwargs={'slug': slug}))
        eq_(response.status_code, 200)

        assert author_email in response.content
        assert blocked_url in response.content

        post_data = {'author_email': author_email,
                     'blocked_url': blocked_url,
                     'open_url': open_url,
                     'slug': slug}

        response = c.post(reverse('bookmarklet:open_document', kwargs={'slug': slug}), post_data)
        eq_(response.status_code, 200)
        obj = OABlockedURL.objects.get(id=obj.id)
        eq_(obj.open_url, open_url)

        self.assertTrue("Your link has been added" in response.content)

    def test_most_common_blocked_url_results(self):
        """
        Create a bunch of blocked URL objects for the same url with
        different open_url results.

        Return the most common open_url.
        """
        self.assertEquals(None, best_open_url(MOCK_URL))
        OABlockedURL.objects.create(slug='foo',
                                    author_email='foo@bar.com',
                                    blocked_url=MOCK_URL,
                                    open_url='http://this.is.good/')

        OABlockedURL.objects.create(slug='foo',
                                    author_email='foo@bar.com',
                                    blocked_url=MOCK_URL,
                                    open_url='http://this.is.bad/')

        OABlockedURL.objects.create(slug='foo',
                                    author_email='foo@bar.com',
                                    blocked_url=MOCK_URL,
                                    open_url='http://this.is.good/')
        self.assertEquals(OABlockedURL.objects.count(), 3)
        self.assertEquals("http://this.is.good/", best_open_url(MOCK_URL))
