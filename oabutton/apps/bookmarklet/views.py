from django.http import HttpResponse, HttpResponseServerError
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from models import Event
from django.conf import settings


try:
    from simplejson import dumps
except:
    from json import dumps

def show_stories(req):
    # we only grab the 50 latest stories
    # the original node code grabbed all stories which will kill your
    # database
    latest_stories = Event.objects.all().order_by('-pub_date')[:50]
    count = Event.objects.count()
    context = {'title': 'Stories', 'events': latest_stories, 'count': count}
    return render(req, 'bookmarklet/site/stories.html', context)


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

        context = {'title': 'Map', 'events': json_data, 'count': count }
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
        url =  req.GET['url']

    if 'doi' in req.GET:
        doi = req.GET['doi']

    c.update({'url': url, 'doi': doi})


    return render_to_response('bookmarklet/index.html', c)

def add_post(req):
    data = req.POST
    event = Event(
            story=data['story'],
            doi=data['doi'],
            url=data['url'],
            profession=data['profession'],
            accessed=data['accessed'],
            )

    lat, lng = data['coords'].split(',')
    event.coords = {'lat': lat, 'lng': lng}

    try:
        event_dict = event.to_dict()
        db = settings.MONGO_DB()
        doc_id = db.events.insert(event_dict)
    except Exception, e:
      return HttpResponseServerError(e)

    scholar_url = ''
    if req.POST['doi']:

        scholar_url = 'http://scholar.google.com/scholar?cluster=http://dx.doi.org/%s' % req.POST['doi']
    return render_to_response('bookmarklet/success.html', {'scholar_url': scholar_url})

