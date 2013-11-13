from django.shortcuts import render_to_response
from django.conf import settings
from django.core.context_processors import csrf
from oabutton.common import SigninForm
import json


def homepage(req):
    # Need to lazy import the Event model so that tests work with
    # mocks
    c = {}
    c.update(csrf(req))

    from oabutton.apps.bookmarklet.models import Event

    evt_count = Event.objects.count()
    data = []

    for evt in Event.objects.all():
        data.append({'doi': evt.doi,
                     'coords': dict(evt.coords),
                     'accessed': evt.accessed.strftime("%b %d, %Y"),
                     'user_name': evt.user_name,
                     'user_profession': evt.user_profession,
                     'description': evt.description,
                     'story': evt.story,
                     'url': evt.url})

    c.update({'count': evt_count,
              'events': json.dumps(data),
              'hostname': settings.HOSTNAME,
              'signin_form': SigninForm()})

    return render_to_response('web/index.jade', c)
