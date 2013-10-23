from datetime import datetime
from django.contrib.auth import get_user_model
from django.core import serializers
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from models import Event
from oabutton.apps.bookmarklet.models import User
from oabutton.common import SigninForm, Bookmarklet
import json


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


@csrf_protect
def signin(request):
    """
    One time signin to create a bookmarklet using HTTP POST.

    The only required field is the email address

    Create a new user and return the URL to the user bookmarklet
    """
    if request.method == 'POST':
        # If the form has been submitted...
        form = SigninForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # TODO: do stuff here
            manager = get_user_model()._default_manager
            data = dict(form.cleaned_data)
            data['username'] = data['email']

            try:
                user = User.objects.get(username=data['email'])
                user.mailinglist = data['mailinglist']
                user.name = data['name']
                user.profession = data['profession']
                user.usernmae = data['username']
                user.save()
            except User.DoesNotExist:
                # Default the username to be email address
                user = manager.create_user(**data)

            return HttpResponse(json.dumps({'url': user.get_bookmarklet_url()}), content_type="application/json")
    return HttpResponseServerError(json.dumps({'errors': form._errors}), content_type="application/json")


def form(req):
    """
    Show the bookmarklet form
    """
    form = Bookmarklet(req.GET)
    if 'url' in form.data:
        # Add readonly and value attributes to the widget
        form.fields['url'].widget.attrs['readonly'] = 'readonly'
        form.fields['url'].widget.attrs['value'] = form.data['url']

    if 'doi' in form.data:
        form.fields['doi'].widget.attrs['readonly'] = 'readonly'
        form.fields['doi'].widget.attrs['value'] = form.data['doi']

    c = {}
    c.update(csrf(req))
    c.update({'bookmarklet': form})

    return render_to_response('bookmarklet/index.html', c)


def add_post(req):
    c = {}
    c.update(csrf(req))

    if req.method == 'POST':
        # If the form has been submitted...
        form = Bookmarklet(req.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            evt_dict = dict(form.cleaned_data)
            lat, lng = evt_dict['coords'].split(',')
            evt_dict['coords'] = {'lat': float(lat), 'lng': float(lng)}
            if evt_dict['accessed'] != '':
                evt_dict['accessed'] = datetime.strptime(evt_dict['accessed'], "%a, %d %b %Y %H:%M:%S %Z")

            event = Event(**evt_dict)
            event.save()

            scholar_url = ''
            if req.POST['doi']:
                scholar_url = 'http://scholar.google.com/scholar?cluster=http://dx.doi.org/%s' % req.POST['doi']
            return render_to_response('bookmarklet/success.html', {'scholar_url': scholar_url, 'oid': str(event.id)})
        else:
            c.update({'bookmarklet': form})
            return render_to_response('bookmarklet/index.html', c)


def generate_bookmarklet(req, user_id):
    return render_to_response('bookmarklet/bookmarklet.html',
                              {'user_id': user_id},
                              content_type="application/javascript")
