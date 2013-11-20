from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from oabutton.apps.web import views as web

urlpatterns = patterns('',
                       url(r'^$', web.homepage, name="homepage"),

                       # I just jammed this in here while i sort out all the URL
                       # mappings.
                       url(r'^api/', include('oabutton.apps.bookmarklet.urls', namespace='bookmarklet')),

                       url(r'^metadata/', include(
                           'oabutton.apps.metadata.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       )
