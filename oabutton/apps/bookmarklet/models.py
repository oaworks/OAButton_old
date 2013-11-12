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
    location = StringField()
    coords = DictField()
    accessed = DateTimeField()
    doi = StringField()
    url = URLField()
    story = StringField()
    description = StringField()
    email = EmailField()

    # This is a lookup to the user object
    user_id = StringField()

    user_name = StringField()
    user_profession = StringField()

class User(mongoengine.django.auth.User):
    """
    This model is modified from mongoengine.django.auth.User
    """
    name = StringField()
    profession = StringField()
    mailinglist = BooleanField()

    def get_bookmarklet_url(self):
        # generate a boilerplate URL for each user
        from django.conf import settings
        return "%s/api/bookmarklet/%s.js" % (settings.HOSTNAME, self.id)
