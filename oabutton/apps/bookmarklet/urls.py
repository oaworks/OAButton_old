from django.conf.urls import patterns, url

from views import form
from views import add_post
from views import generate_bookmarklet
from views import get_json
from views import signin

urlpatterns = patterns('',
                       # I think these 3 should be broken out to an API URL handler so we
                       # can evolve it
                       url(r'^$', get_json, name="get_json"),

                       url(r'^form/$', form, name="form"),

                       url(r'^post/$', add_post, name="add_post"),
                       url(r'^signin/$', signin, name="signin"),
                       url(r'^bookmarklet/(?P<user_id>.*).js$',
                           generate_bookmarklet,
                           name="generate_bookmarklet"))
