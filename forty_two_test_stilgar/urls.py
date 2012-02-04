from django.conf.urls.defaults import patterns, include, url
from forty_two_test_stilgar.apps.frontpage_profile.views \
        import frontpage_profile

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', frontpage_profile),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
