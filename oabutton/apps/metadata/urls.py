from django.conf.urls import patterns, url

from views import core_search

urlpatterns = patterns('',
                       url(r'^coresearch.json/(.*)$', core_search, name='core-search'))
