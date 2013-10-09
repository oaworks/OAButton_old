from django.http import HttpResponse, HttpResponseServerError
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.core import serializers
from models import Event
from django.conf import settings


def show_stories(req):
    # we only grab the 50 latest stories
    # the original node code grabbed all stories which will kill your
    # database
    latest_stories = Event.objects.all().order_by('-pub_date')[:50]
    count = Event.objects.count()
    context = {'title': 'Stories', 'events': latest_stories, 'count': count}
    return render_to_response('bookmarklet/site/stories.html', context)


def show_map(req):
    # TODO: we need to make this smarter.  Coallescing the lat/long
    # data on a nightly basis and folding that down into clustered
    # points would mean we throw less data down to the browser
    try:
        db = settings.MONGO_DB()
        all_events = [evt for evt in db.events.find()]

        # TODO: use a mongo count function here
        count = len(all_events)

        # TODO: Need to do this an async call and roll up stuff using
        # clustering
        json_data = serializers.serialize("json", all_events)

        context = {'title': 'Map', 'events': json_data, 'count': count}
        return render_to_response(req, 'bookmarklet/site/map.html', context)
    except Exception, e:
        return HttpResponseServerError(e)


def get_json(req):
    # Dump all data as JSON.  This seems like a terrible idea when the
    # dataset gets large.
    json_data = serializers.serialize("json", Event.objects.all())
    return HttpResponse(json_data, content_type="application/json")


def add(req):
    c = {}
    c.update(csrf(req))
    # Display an entry page
    # How does the DOI get in automatically?  This seems really wrong.
    # At the least, we need a test here to illustrate why this should
    # work at all.

    # TODO: use a form thing here
    doi = ''
    url = ''
    if 'url' in req.GET:
        url = req.GET['url']

    if 'doi' in req.GET:
        doi = req.GET['doi']

    c.update({'url': url, 'doi': doi})

    return render_to_response('bookmarklet/index.html', c)


def convert_post(data, event):
    """
    Serialize a HTTP POST dict and write it to an Event object
    """
    for k, v in data.items():
        if k == 'coords':
            # Skip coordinates
            continue
        setattr(event, k, v)
    lat, lng = data['coords'].split(',')
    event.coords = {'lat': lat, 'lng': lng}


def add_post(req):
    event = Event()
    convert_post(req.POST, event)

    try:
        event_dict = event.to_dict()
        db = settings.MONGO_DB()
        db.events.insert(event_dict)
    except Exception, e:
        return HttpResponseServerError(e)

    c = {'doi': req.POST['doi']}

    return render_to_response('bookmarklet/success.html', c)
