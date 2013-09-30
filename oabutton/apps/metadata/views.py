from django.http import HttpResponse
from os import environ
import requests
import logging
import json

CORE_API_BASE = 'http://core.kmi.open.ac.uk/api'
CORE_API_SEARCH = CORE_API_BASE + '/search/'
CORE_API_KEY = environ['CORE_API_KEY']

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def core_search(req, query):
    parameters = req.GET.copy()
    parameters['api_key'] = CORE_API_KEY
    parameters['format'] = 'json'

    query_url = CORE_API_SEARCH + query

    logger.debug(query_url)

    r = requests.get(query_url, params=parameters)

    logger.debug('Response from CORE: %i', r.status_code)

    if r.status_code == requests.codes.ok:
        return HttpResponse(r.text, content_type='application/json')
    else:
        error_info = {'error': {
            'status': r.status_code,
            'content': r.text
        }}
        return HttpResponse(json.dumps(error_info),
                            content_type='application/json',
                            status=requests.codes.bad_gateway)
