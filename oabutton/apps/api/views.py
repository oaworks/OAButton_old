from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.shortcuts import render_to_response
from oabutton.apps.bookmarklet.models import OAUser, OAEvent
from oabutton.apps.bookmarklet.models import best_open_url
from oabutton.util import deprecated
from validate_email import validate_email
import datetime
import json
import re
import requests


"""
Tokens are defined by uuid4 with no dashes:

    var guid = function() {
        return 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g,
        function(c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });
    }

    A sample token looks like: '6d2b0a7e-5d50-470e-b014-94017771dc75'
"""

hex_re = re.compile("^[0-9a-f]+$")


def register(req):
    """
    Expects a POST with {'email': email, 'token': token}, returns
    either a 200 or 404
    """
    post_data = json.load(req.POST)
    email, token, err = check_security(post_data)
    if err:
        return err

    user = OAUser.objects.create(email=email,
                                 slug=token,
                                 mailinglist=post_data['mailinglist'])
    user.save()
    user.send_confirmation_email()
    return HttpOKJson()


def am_i_registered(req):
    """
    Expects a POST with {'email': email, 'token': token}, returns
    either a 200 or 404
    """
    post_data = json.load(req.POST)
    email, token, err = check_security(post_data)
    if err:
        return err

    if not _verify_email_confirmed(email, token):
        return HttpUnauthorized()

    return HttpOKJson()


def blocked(req):
    """
    registers a new OAEvent
    """
    post_data = json.load(req.POST)
    email, token, err = check_security(post_data)
    if err:
        return err

    try:
        user = OAUser.objects.get(slug=token, email=email)
        evt_dict = {}
        evt_dict['coords_lat'] = float(post_data['coords_lat'])
        evt_dict['coords_lng'] = float(post_data['coords_lng'])
        evt_dict['accessed'] = datetime.datetime.now()

        evt_dict['user_email'] = user.email
        evt_dict['user_name'] = user.name
        evt_dict['user_profession'] = user.profession

        event = OAEvent.objects.create(**evt_dict)
        event.save()
        return HttpOKJson()
    except Exception, e:
        jdata = json.dumps({'errors': [str(e)]})
        return HttpResponseServerError(jdata,
                                       content_type="application/json")


def oa_status(req):
    """
    Find an OA version of a URL.

    POST a blob like this:

        {'email': email,
         'token': token,
         'url': url}

    You'll get a HTTP 200 with the URL as the response,
    or an HTTP 200 with *no* URL.  Not
    """
    post_data = json.load(req.POST)
    email, token, err = check_security(post_data)
    if err:
        return err

    url = post_data['url']

    open_url = best_open_url(url)
    result = {'status': 'ok'}
    if open_url is not None:
        result.update({'open_url': open_url})

    return HttpResponse(json.dumps(result),
                        content_type="application/json")


def doi_stumble(req):
    post_data = json.load(req.POST)
    email, token, err = check_security(post_data)
    if err:
        return err


#
#
# ============================== private and deprecated functions
# below
#
#

def _verify_email_confirmed(email, token):
    try:
        user = OAUser.objects.get(slug=token, email=email)
        if user.email_confirmed:
            return True
    except:
        # Who cares. Just continue along.
        return False


@deprecated
def _xref_proxy(req, doi):
    """

    This was only needed historically because of the bookmarklet.

    Bookmarklets have weird cross-domain rules.  The addon should make this request directly
    instead and pass the data back into the calling script.

    $ curl -LH "Accept: application/rdf+xml;q=0.5, application/vnd.citationstyles.csl+json;q=1.0" http://dx.doi.org/10.1126/scisignal.2004518

    Sample response:
        {u'DOI': u'10.1126/scisignal.2004518',
         u'ISSN': [u'1945-0877', u'1937-9145'],
         u'URL': u'http://dx.doi.org/10.1126/scisignal.2004518',
         u'author': [{u'family': u'Sardesai', u'given': u'N.'},
          {u'family': u'Lee', u'given': u'L.-Y.'},
          {u'family': u'Chen', u'given': u'H.'},
          {u'family': u'Yi', u'given': u'H.'},
          {u'family': u'Olbricht', u'given': u'G. R.'},
          {u'family': u'Stirnberg', u'given': u'A.'},
          {u'family': u'Jeffries', u'given': u'J.'},
          {u'family': u'Xiong', u'given': u'K.'},
          {u'family': u'Doerge', u'given': u'R. W.'},
          {u'family': u'Gelvin', u'given': u'S. B.'}],
         u'container-title': u'Science Signaling',
         u'deposited': {u'date-parts': [[2013, 12, 17]], u'timestamp': 1387238400000},
         u'indexed': {u'date-parts': [[2014, 5, 23]], u'timestamp': 1400848880311},
         u'issue': u'302',
         u'issued': {u'date-parts': [[2013, 11, 19]]},
         u'member': u'http://id.crossref.org/member/221',
         u'page': u'ra100-ra100',
         u'prefix': u'http://id.crossref.org/prefix/10.1126',
         u'publisher': u'American Association for the Advancement of Science (AAAS)',
         u'reference-count': 58,
         u'score': 1.0,
         u'source': u'CrossRef',
         u'subject': [u'Medicine(all)'],
         u'subtitle': [],
         u'title': u'Cytokinins Secreted by Agrobacterium Promote Transformation by Repressing a Plant Myb Transcription Factor',
         u'type': u'journal-article',
         u'volume': u'6'}
    """
    url = "http://data.crossref.org/%s" % doi
    headers = {'Accept': "application/rdf+xml;q=0.5, application/vnd.citationstyles.csl+json;q=1.0"}
    r = requests.get(url, headers=headers)
    return HttpResponse(r.text, content_type="application/json")


def HttpOKJson():
    return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")


def HttpUnauthorized():
    return HttpResponse('Unauthorized', status=401)


def verify_token(token):
    if not (len(token) == 32):
        return False

    # Check they're all hex
    try:
        int("0x%s" % token, 0)
    except:
        return False
    return True


def check_security(post_data):
    email = post_data['email']
    token = post_data['token']

    if not validate_email(email):
        jdata = json.dumps({'errors': ["Invalid email address"]})
        return "", "", HttpResponseServerError(jdata,
                                               content_type="application/json")

    if not verify_token(token):
        jdata = json.dumps({'errors': ["Invalid token"]})
        return "", "", HttpResponseServerError(jdata,
                                               content_type="application/json")

    if not _verify_email_confirmed(email, token):
        return "", "", HttpUnauthorized()

    return email, token, None


def apidocs(req):
    return render_to_response('api/docs.html')
