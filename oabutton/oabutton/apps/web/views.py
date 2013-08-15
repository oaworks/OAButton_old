from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.core import serializers

try:
    from simplejson import dumps
except:
    from json import dumps


def homepage(req):
    return render(req, 'web/index.html')
