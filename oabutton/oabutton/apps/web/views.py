from django.http import HttpResponse, HttpResponseServerError
from django.core import serializers
from django.shortcuts import render_to_response
from django.core import serializers
from django.conf import settings

from json import dumps
from json import JSONEncoder
from bson.objectid import ObjectId

class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:            
            return JSONEncoder.default(obj, **kwargs)

def homepage(req):
    db = settings.MONGO_CLIENT.oabutton_db
    
    # TODO: this needs to get cleaned up to not eat all memory

    data = [obj for obj in db.events.find()]

    return render_to_response('web/index.html', 
            {'events': dumps(data, cls=MongoEncoder)})
