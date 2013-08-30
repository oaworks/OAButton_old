from django.http import HttpResponse, HttpResponseServerError
from django.core import serializers
from django.shortcuts import render_to_response
from django.core import serializers
from django.conf import settings

from json import dumps
from json import JSONEncoder
from bson.objectid import ObjectId
import datetime

from django.contrib.sites.models import Site


class MyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)

def homepage(req):
    # TODO: this needs to get cleaned up to not eat all memory

    current_site = Site.objects.get_current()

    try:
        db = settings.MONGO_DB()
        all_events = [evt for evt in db.events.find()]

        # TODO: Need to do this an async call and roll up stuff using
        # clustering
        json_data = dumps(all_events, cls=MyEncoder)
    except Exception, e:
        # Don't error out, just don't bother loading any data
        json_data = []

    return render_to_response('web/index.html',
            {'events': json_data, 
             'hostname': current_site.domain})



