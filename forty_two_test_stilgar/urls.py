from django.conf.urls.defaults import patterns, include, url
from apps.user_profile.views import user_profile

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', user_profile),
        url(r'^request-log/',
                include('forty_two_test_stilgar.apps.request_logger.urls')),
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^admin/', include(admin.site.urls)),
    )
