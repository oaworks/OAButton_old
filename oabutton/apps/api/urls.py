from django.conf.urls import patterns, url

from views import register, blocked, oa_status
from views import am_i_registered, doi_stumble
from views import apidocs

urlpatterns = patterns('',
                       url(r'$', apidocs, name="apidocs"),
                       url(r'^register/$', register, name="register"),
                       url(r'^am_i_registered/$', am_i_registered, name="am_i_registered"),
                       url(r'^blocked/$', blocked, name="blocked"),
                       url(r'^oa_status/$', oa_status, name="oa_status"),
                       url(r'^doi_stumble/$', doi_stumble, name="doi_stumble"),
                       )
