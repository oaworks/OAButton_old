from mongoengine import DateTimeField
from mongoengine import DictField
from mongoengine import Document
from mongoengine import EmailField
from mongoengine import StringField
from mongoengine import URLField
from mongoengine import BooleanField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import check_password, make_password
from mongoengine.django.utils import datetime_now
import mongoengine.django.auth

class Event(Document):
    # Note that this has a lowercase 'e' to maintain compatibility
    meta = {'collection': 'events'}
    name = StringField()
    profession = StringField()
    location = StringField()
    coords = DictField()
    accessed = DateTimeField()
    pub_date = DateTimeField()
    doi = StringField()
    url = URLField()
    story = StringField()
    email = EmailField()

class User(mongoengine.django.auth.User):
    """
    This model is modified from mongoengine.django.auth.User
    """
    def get_bookmarklet_url(self):
        # generate a boilerplate URL for each user
        from django.conf import settings
        return "%s/api/bookmarklet/%s.js" % (settings.HOSTNAME, self.id)
