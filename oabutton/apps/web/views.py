from django.shortcuts import render_to_response
from django.conf import settings
from oabutton.apps.bookmarklet.models import Event

from json import dumps

from oabutton.json_util import MyEncoder


def homepage(req):
    evt_count = Event.objects.count()
    json_data = Event.objects.all().to_json()
    return render_to_response('web/index.html',
                              {'count': evt_count,
                               'events': json_data,
                               'hostname': 'localhost'}) # TODO: change HOSTNAME
