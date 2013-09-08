from django.http import HttpResponse, HttpResponseServerError
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.core import serializers
from models import Event
from django.conf import settings
from datetime import datetime

def show_map(req):
    # TODO: we need to make this smarter.  Coallescing the lat/long
    # data on a nightly basis and folding that down into clustered
    # points would mean we throw less data down to the browser
    json_data = Event.objects.all().to_json()
    count = Event.objects.count()
    context = {'title': 'Map', 'events': json_data, 'count': count}
    return render_to_response(req, 'bookmarklet/site/map.html', context)

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

def add_post(req):
    evt_dict = {}
    for k in Event._fields.keys():
        if k == 'id':
            continue
        evt_dict[k] = req.POST.get(k, '')

        if evt_dict[k] == '':
            evt_dict[k] = None

    lat, lng = evt_dict['coords'].split(',')
    evt_dict['coords'] = {'lat': float(lat), 'lng': float(lng)}
    if evt_dict['accessed'] != '':
        evt_dict['accessed'] = datetime.strptime(evt_dict['accessed'], "%a, %d %b %Y %H:%M:%S %Z")

    event = Event(**evt_dict)
    event.save()

    scholar_url = ''
    if req.POST['doi']:
        scholar_url = 'http://scholar.google.com/scholar?cluster=http://dx.doi.org/%s' % req.POST[
            'doi']
    return render_to_response('bookmarklet/success.html', {'scholar_url': scholar_url, 'oid': str(event.id)})

def generate_bookmarklet(req, user_id): 
    return render_to_response('bookmarklet/bookmarklet.html',
            {'user_id': user_id}, content_type="application/javascript")
