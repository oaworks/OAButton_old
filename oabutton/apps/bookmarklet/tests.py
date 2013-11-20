"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from nose.tools import eq_, ok_
from oabutton.apps.bookmarklet.models import OAEvent, OAUser
import datetime
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
        response = c.post('/api/post/', POST_DATA)

        assert response.status_code == 302

        evt = OAEvent.objects.get(id=c.session['data']['event_id'])

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
        response = c.post('/api/post/', POST_DATA)

        assert response.status_code == 302

        evt = OAEvent.objects.get(id=c.session['data']['event_id'])

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
        response = c.post('/api/post/', POST_DATA)

        assert response.status_code == 302

        data = OAEvent.objects.get(id=c.session['data']['event_id'])
        eq_(data.coords, {'lat': 44.0, 'lng': -79.5})
        eq_(data.doi, '10.1016/j.urology.2010.05.009.')
        eq_(data.url, 'http://www.ncbi.nlm.nih.gov/pubmed/20709373')

        actual_date = data.accessed
        eq_(actual_date.year, 2013)
        eq_(actual_date.month, 9)
        eq_(actual_date.day, 9)

        eq_(data.user_name, 'some name')
        eq_(data.user_profession, 'Student')
        eq_(data.story, 'some access requirement')

        # Check that we can resolve the original user oid
        evt = OAEvent.objects.filter(id=c.session['data']['event_id'])[0]
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
        response = c.post('/api/post/', POST_DATA)

        response = c.post('/api/form/page3/')
        # Check that the DOI is passed through correctly
        data_doi_re = re.compile('<body [^>]*data-doi="%s">'
                                 % POST_DATA['doi'])
        assert data_doi_re.search(response.content) is not None

    def test_data_xref_proxy(self):
        # TODO: Need a proper test for this that doesn't clobber the
        # network. Inject a fake requests mock object into xref_proxy
        # prior to execution
        pass
        """
        c = Client()
        response = c.get('/api/xref_proxy/10.1103/PhysRevD.15.2752')
        assert json.loads(response.content) != None
        """
