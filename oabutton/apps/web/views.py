from django.shortcuts import render_to_response
from django.conf import settings

from json import dumps

from django.contrib.sites.models import Site

from oabutton.json_util import MyEncoder


def homepage(req):
    # TODO: this needs to get cleaned up to not eat all memory

    current_site = Site.objects.get_current()

    db = settings.MONGO_DB()
    all_events = [evt for evt in db.events.find()]

    # TODO: Need to do this an async call and roll up stuff using
    # clustering
    json_data = dumps(all_events, cls=MyEncoder)

    return render_to_response('web/index.html',
                              {'count': len(all_events),
                               'events': json_data,
                               'hostname': current_site.domain})
