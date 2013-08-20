from django.http import HttpResponse, HttpResponseServerError
from django.core import serializers
from django.shortcuts import render_to_response
from django.core import serializers

from oabutton.apps.bookmarklet.models import Event

try:
    from simplejson import dumps
except:
    from json import dumps


def homepage(req):
    data = serializers.serialize("json", Event.objects.all())
    return render_to_response('web/index.html', {'events': data})
