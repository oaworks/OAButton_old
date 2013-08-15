from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from oabutton.apps.bookmarklet import views as bm
from oabutton.apps.web import views as web

urlpatterns = patterns('',
    url(r'^$', web.homepage, name="homepage"),

    #url(r'^about/$', bm.about, name="about"),
    #url(r'^stories/$', bm.show_stories, name="show_stories"),
    #url(r'^map/$', bm.show_map, name="show_map"),

    # this has been moved to /api
    #url(r'^download.json$', bm.get_json, name="get_json"),

    # I just jammed this in here while i sort out all the URL
    # mappings.
    #url(r'^bookmarklet/', include('oabutton.apps.bookmarklet.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
