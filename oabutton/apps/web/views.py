from django.shortcuts import render_to_response
from django.conf import settings
from oabutton.common import SigninForm, teamdata, thanksdata
import json


def homepage(req):
    # Need to lazy import the OAEvent model so that tests work with
    # mocks
    c = {}

    from oabutton.apps.bookmarklet.models import OAEvent

    evt_count = OAEvent.objects.count()
    data = []

    for evt in OAEvent.objects.all():
        data.append({'doi': evt.doi,
                     'coords': dict(evt.coords),
                     'accessed': evt.accessed.strftime("%b %d, %Y"),
                     'user_name': evt.user_name,
                     'user_profession': evt.user_profession,
                     'description': evt.description,
                     'story': evt.story,
                     'url': evt.url,
                     })

    c.update({'DEBUG': settings.DEBUG,
              'count': evt_count,
              'events': json.dumps(data),
              'hostname': settings.HOSTNAME,
              'signin_form': SigninForm(),
              'team_data': teamdata,
              'thanks_data': thanksdata})

    return render_to_response('web/start.jade', c)
