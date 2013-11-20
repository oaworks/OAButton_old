from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from models import OAEvent, OAUser
from oabutton.common import SigninForm, Bookmarklet
import dateutil.parser
import json
import requests
import uuid


def show_map(req):
    # TODO: we need to make this smarter.  Coallescing the lat/long
    # data on a nightly basis and folding that down into clustered
    # points would mean we throw less data down to the browser
    json_data = OAEvent.objects.all().to_json()
    count = OAEvent.objects.count()
    context = {'title': 'Map', 'events': json_data, 'count': count}
    return render_to_response(req, 'bookmarklet/site/map.html', context)


@csrf_protect
@require_http_methods(["POST"])
def signin(request):
    """
    One time signin to create a bookmarklet using HTTP POST.

    The only required field is the email address

    Create a new user and return the URL to the user bookmarklet
    """
    # If the form has been submitted...
    form = SigninForm(request.POST)  # A form bound to the POST data
    if form.is_valid():  # All validation rules pass
        data = dict(form.cleaned_data)

        user = OAUser.objects.create(name=data['name'],
                email=data['email'],
                profession=data['profession'],
                slug = uuid.uuid4().hex,
                mailinglist = data['mailinglist'],
                )
        user.save()

        return HttpResponse(json.dumps({'url': user.get_bookmarklet_url()}), content_type="application/json")
    return HttpResponseServerError(json.dumps({'errors': form._errors}), content_type="application/json")


def form1(req, slug):
    """
    Show the bookmarklet form
    """
    form = Bookmarklet(req.GET)

    if 'doi' in form.data:
        form.fields['doi'].widget.attrs['readonly'] = 'readonly'
        form.fields['doi'].widget.attrs['value'] = form.data['doi']

    if 'url' in form.data:
        form.fields['url'].widget.attrs['value'] = form.data['url']

    form.fields['slug'].widget.attrs['value'] = slug

    c = {}
    s = req.session
    s['slug'] = slug

    c.update(csrf(req))
    c.update({'bookmarklet': form, 'slug': slug})
    return render_to_response('bookmarklet/page1.html', c,
                              context_instance=RequestContext(req))


def form2(req):
    """
    Show the bookmarklet form. We just need the CSRF token here.
    """
    s = req.session
    data = s['data']
    scholar_url = data['scholar_url']
    doi = data['doi']
    event = OAEvent.objects.get(id=data['event_id'])

    c = {}
    c.update(csrf(req))
    c.update({'scholar_url': scholar_url, 'doi': doi, 'url': event.url})
    return render_to_response('bookmarklet/page2.html', c,
                              context_instance=RequestContext(req))


def form3(req):
    """
    Show the bookmarklet form
    """

    s = req.session
    if req.method != 'POST':
        return redirect('bookmarklet:form1', slug=s['slug'])

    data = s['data']
    scholar_url = data['scholar_url']
    doi = data['doi']
    event = OAEvent.objects.get(id=data['event_id'])

    c = {}
    c.update(csrf(req))
    c.update({'scholar_url': scholar_url, 'doi': doi, 'url': event.url})
    return render_to_response('bookmarklet/page3.html', c,
                              context_instance=RequestContext(req))


def add_post(req):
    c = {}
    c.update(csrf(req))

    s = req.session
    if req.method == 'POST':
        # If the form has been submitted...
        form = Bookmarklet(req.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            evt_dict = dict(form.cleaned_data)
            lat, lng = evt_dict['coords'].split(',')
            evt_dict['coords'] = {'lat': float(lat), 'lng': float(lng)}
            if evt_dict['accessed'] != '':
                evt_dict['accessed'] = dateutil.parser.parse(evt_dict['accessed'])

            user = OAUser.objects.get(slug=evt_dict['slug'])
            evt_dict['user_email'] = user.email
            evt_dict['user_name'] = user.name
            evt_dict['user_profession'] = user.profession

            evt_dict['user_slug'] = user.slug
            del evt_dict['slug']

            event = OAEvent.objects.create(**evt_dict)
            event.save()

            scholar_url = ''
            if 'doi' in evt_dict:
                # Some dumb DOIs end with '.' characters
                while evt_dict['doi'].endswith('.'):
                    evt_dict['doi'] = evt_dict['doi'][:-1]
                doi = evt_dict['doi']
                scholar_url = 'http://scholar.google.com/scholar?cluster=http://dx.doi.org/%s' % doi

            s['data'] = {'event_id': event.id,
                                   'scholar_url': scholar_url,
                                   'doi': doi}

            return redirect('bookmarklet:form2')
        else:
            return redirect('bookmarklet:form1', slug=s['slug'])


def xref_proxy(req, doi):
    url = "http://data.crossref.org/%s" % doi
    headers = {'Accept': "application/vnd.citationstyles.csl+json"}
    r = requests.get(url, headers=headers)
    return HttpResponse(r.text, content_type="application/json")

def xref_proxy_simple(req, doi):
    url = "http://data.crossref.org/%s" % doi
    headers = {'Accept': "application/json"}
    r = requests.get(url, headers=headers)
    return HttpResponse(r.text, content_type="application/json")


def generate_bookmarklet(req, slug):
    return render_to_response('bookmarklet/bookmarklet.html',
                              {'slug': slug},
                              content_type="application/javascript")
