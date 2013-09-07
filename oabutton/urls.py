from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from oabutton.apps.bookmarklet import views as bm
from oabutton.apps.web import views as web

urlpatterns = patterns('',
    url(r'^$', web.homepage, name="homepage"),

    # I just jammed this in here while i sort out all the URL
    # mappings.
    url(r'^api/', include('oabutton.apps.bookmarklet.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
