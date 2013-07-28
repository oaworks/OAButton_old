from django.conf.urls import patterns, include, url

from views import show_stories, show_map
from views import add, add_post, get_json

urlpatterns = patterns('',

    # I think these 3 should be broken out to an API URL handler so we
    # can evolve it
    url(r'^get_json/$', get_json, name="get_json"),
    url(r'^add/$', add, name="add"),
    url(r'^post/$', add_post, name="add_post"),
)

