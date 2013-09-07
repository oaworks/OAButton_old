from django.conf.urls import patterns, url

from views import add, add_post, get_json

urlpatterns = patterns('',
                       # I think these 3 should be broken out to an API URL handler so we
                       # can evolve it
                       url(r'^$', get_json, name="get_json"),
                       url(r'^add/$', add, name="add"),
                       url(r'^post/$', add_post, name="add_post"))
