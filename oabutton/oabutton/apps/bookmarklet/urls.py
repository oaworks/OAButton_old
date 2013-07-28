from django.conf.urls import patterns, include, url

from views import show_stories

urlpatterns = patterns('',
    url(r'^show_stories/$', show_stories, name="show_stories"),
)

