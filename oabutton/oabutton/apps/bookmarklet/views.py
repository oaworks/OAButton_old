from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.core import serializers
from models import Event

try:
    from simplejson import dumps
except:
    from json import dumps

# TODO: we should really break up the view URLs here to separate the
# OAButton facing website from the bookmarklet URLs.

def show_stories(req):
    # we only grab the 50 latest stories
    # the original node code grabbed all stories which will kill your
    # database
    latest_stories = Event.objects.all().order_by('-pub_date')[:50]
    count = Event.objects.count()
    context = {'events': latest_stories, 'count': count}
    return render(req, 'bookmarklet/stories.html', context)


def show_map(req):
    # TODO: we need to make this smarter.  Coallescing the lat/long
    # data on a nightly basis and folding that down into clustered
    # points would mean we throw less data down to the browser
    count = Event.objects.count()
    json_data = serializers.serialize("json", Event.objects.all())
    context = {title: 'Map', events: json_data, count: count }
    return render(req, 'bookmarklet/map.html', context)


def get_json(req):
    # Dump all data as JSON.  This seems like a terrible idea when the
    # dataset gets large.
    json_data = serializers.serialize("json", Event.objects.all())
    return HttpResponse(json_data, content_type="application/json")

def add(req):
  # How does the DOI get in automatically?  This seems really wrong.
  # At the least, we need a test here to illustrate why this should
  # work at all.
  return render('sidebar/index.html', context={'url': req.query.url, 'doi': req.query.doi})

def post(req):
    # Handle POST
    event = Event()
    # Where does the coords come from? This seems like it's using the
    # HTML5 locationAPI.  Need to dig around a bit
    coords = req['coords'].split(',')

    event.coords_lat = float(coords[0])
    event.coords_lng = float(coords[1])
    try:
        event.save()
    except Exception, e:
      return HttpResponseServerError(e)

    scholar_url = ''
    if req.body['doi']:
        scholar_url = 'http://scholar.google.com/scholar?cluster=' + 'http://dx.doi.org/' + req['doi']
    return render('sidebar/success.html', {'scholar_url': scholar_url})

