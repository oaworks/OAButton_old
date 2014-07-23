from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.shortcuts import render_to_response
from oabutton.apps.bookmarklet.models import OAUser, OAEvent
from oabutton.apps.bookmarklet.models import best_open_url
from validate_email import validate_email
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
        #evt_dict['coords_lat'] = float(post_data['coords_lat'])
        #evt_dict['coords_lng'] = float(post_data['coords_lng'])
        #evt_dict['accessed'] = datetime.datetime.now()

        evt_dict['doi'] = post_data['doi']
        evt_dict['url'] = post_data['url']

        # Backfilled from user data
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

    Response :

    {
    'status': 'ok',
    'open_url': url ,  # will be an empty string if none available
    'block_count': 10
    }


    }
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
    else:
        result.update({'open_url': ''})
    result.update({'blocked_count': OAEvent.objects.filter(url=url).count()})

    return HttpResponse(json.dumps(result),
                        content_type="application/json")


def doi_stumble(req):
    post_data = json.load(req.POST)
    email, token, err = check_security(post_data)
    if err:
        return err
    # TODO: just accept everything for now.  I'll sort this out later.
    return HttpOKJson()


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
