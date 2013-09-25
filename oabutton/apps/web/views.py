from django.shortcuts import render_to_response
from django.conf import settings
from oabutton.json_util import MyEncoder

def homepage(req):
    # Need to lazy import the Event model so that tests work with
    # mocks
    from oabutton.apps.bookmarklet.models import Event

    evt_count = Event.objects.count()
    json_data = Event.objects.all().to_json()
    return render_to_response('web/index.html',
                              {'count': evt_count,
                               'events': json_data,
                               'hostname': settings.HOSTNAME})
