from django.core.urlresolvers import reverse
from django.db import connection
from django.db import models
from oabutton.apps.template_email import TemplateEmail

import binascii
import datetime
import os
import requests


class OAEvent(models.Model):
    location = models.CharField(max_length=200, null=True, blank=True)

    coords_lat = models.FloatField()
    coords_lng = models.FloatField()

    def _get_coords(self):
        return {'lat': self.coords_lat, 'lng': self.coords_lng}

    def _set_coords(self, value):
        self.coords_lat = value['lat']
        self.coords_lng = value['lng']

    coords = property(_get_coords, _set_coords)

    accessed = models.DateTimeField()
    doi = models.TextField()
    url = models.URLField(max_length=2000, db_index=True)
    story = models.TextField(null=True, blank=True)
    description = models.TextField()

    # This is a lookup to the user object
    user_slug = models.CharField(max_length=40, db_index=True)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=200)
    user_profession = models.CharField(max_length=200)


class OAUser(models.Model):
    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(db_index=True, null=False)
    email_confirmed = models.BooleanField(default=False)

    profession = models.CharField(max_length=200)
    mailinglist = models.BooleanField()

    slug = models.CharField(unique=True, max_length=40)

    salt = models.CharField(max_length=12, null=True)

    def get_confirm_path(self):
        return reverse('bookmarklet:email_confirm',
                       kwargs={'slug': self.slug,
                               'salt': self.salt})

    def send_confirmation_email(self):
        from django.conf import settings
        self.salt = binascii.b2a_hex(os.urandom(15))[:12]
        self.save()

        context = {'hostname': settings.HOSTNAME,
                   'confirm_url': self.get_confirm_path()}

        email = TemplateEmail(template='bookmarklet/email_confirmation.html',
                              context=context,
                              from_email=settings.OABUTTON_EMAIL,
                              to=[self.email])
        email.send()

    def get_bookmarklet_url(self):
        # generate a boilerplate URL for each user
        from django.conf import settings
        return "%s/api/bookmarklet/%s.js" % (settings.HOSTNAME, self.slug)


class OASession(models.Model):
    key = models.CharField(max_length=40)
    data = models.TextField()
    expire = models.FloatField()


class OABlockedURL(models.Model):
    slug = models.CharField(max_length=40, db_index=True)
    author_email = models.EmailField(db_index=True)
    blocked_url = models.URLField(max_length=2000, db_index=True)
    open_url = models.URLField(max_length=2000, db_index=True)

    created = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

    def check_oa_url(self):
        """
        Check that the Open Access URL is at least readable (HTTP
        200).

        Any HTTP error or status != 200 will clear the open_url
        setting.
        """
        if self.open_url:
            try:
                r = requests.get(self.open_url)
                # Any 2xx status is ok
                if str(r.status_code)[0] == '2':
                    return True, None
                else:
                    invalid = InvalidOALink(url=self.open_url, src=self)
                    invalid.save()
                    self.open_url = ""
                    self.save()
                    return False, requests.exceptions.HTTPError(status=r.status_code)
            except Exception, e:
                self.open_url = ""
                self.save()
                return False, e
        return False, RuntimeError("No Open URL is set")


class InvalidOALink(models.Model):
    src = models.ForeignKey(OABlockedURL)
    url = models.URLField(max_length=2000)


def best_open_url(blocked_url):
    cursor = connection.cursor()
    try:
        cursor.execute("""
        select count(open_url) open_count, open_url from
        bookmarklet_oablockedurl where blocked_url = %s group by open_url order by open_count desc
        """, [blocked_url])
        if cursor.rowcount:
            row = cursor.fetchone()
            return row[1]
        else:
            return None
    finally:
        cursor.close()
