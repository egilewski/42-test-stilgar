from django.conf.urls.defaults import patterns, include, url
from forty_two_test_stilgar.apps.request_logger.views import \
        simulate_http_status
from django.views.generic import list_detail
from forty_two_test_stilgar.apps.request_logger.models import Request

request_log_list_info = {
        'queryset': Request.objects.all(),
        'template_object_name': 'request',
        'template_name': 'request_logger_list.html',
    }
request_log_detail_info = {
        'queryset': Request.objects.all(),
        'template_object_name': 'request',
        'template_name': 'request_logger_detail.html',
    }

urlpatterns = patterns('',
        url(r'^testing/(?P<status>\d{3})/$', simulate_http_status),
        url(r'^$', list_detail.object_list, request_log_list_info),
        url(r'^(?P<object_id>\d+)/$', list_detail.object_detail,
                request_log_detail_info),
    )
