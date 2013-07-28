from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from oabutton.apps.bookmarklet import views as bm

urlpatterns = patterns('',
    url(r'^$', bm.homepage, name="homepage"),
    url(r'^about/$', bm.about, name="about"),
    url(r'^stories/$', bm.show_stories, name="show_stories"),
    url(r'^map/$', bm.show_map, name="show_map"),

    url(r'^bookmarklet/', include('oabutton.apps.bookmarklet.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
