"""
Run this from : 

    python manage.py shell


"""

from pymongo import MongoClient
import json
from bson.objectid import ObjectId

import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min +
                    obj).time().isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return super(DateTimeEncoder, self).default(obj)

client = MongoClient()
db = client['oabutton-server-dev']

encoder = DateTimeEncoder()

with open('/tmp/users.json', 'w') as user_file:
    for u in db.user.find():
        user_file.write(encoder.encode(u)+'\n')

with open('/tmp/events.json', 'w') as event_file:
    for e in db.events.find():
        event_file.write(encoder.encode(e) + '\n')
