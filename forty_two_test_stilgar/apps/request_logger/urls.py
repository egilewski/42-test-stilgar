from django.conf.urls.defaults import patterns, include, url
from forty_two_test_stilgar.apps.request_logger.views import \
        simulate_http_status

urlpatterns = patterns('',
    url(r'^testing/(?P<status>\d{3})/$', simulate_http_status),
)
