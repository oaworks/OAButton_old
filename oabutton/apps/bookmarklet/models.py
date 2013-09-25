from mongoengine import DateTimeField
from mongoengine import DictField
from mongoengine import Document
from mongoengine import EmailField
from mongoengine import StringField
from mongoengine import URLField

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
