"""Request logger app's urlconf."""
from django.conf.urls.defaults import patterns, url
from forty_two_test_stilgar.apps.request_logger.views import \
        simulate_http_status
from django.views.generic import list_detail
from forty_two_test_stilgar.apps.request_logger.models import Request

REQUEST_LOG_LIST_INFO = {
    'queryset': Request.objects.order_by('-priority', '-id'),
    'template_object_name': 'request_record',
    'template_name': 'request_logger_list.html',
    'paginate_by': 20,
}
REQUEST_LOG_DETAIL_INFO = {
    'queryset': Request.objects.all(),
    'template_object_name': 'request_record',
    'template_name': 'request_logger_detail.html',
}

# pylint: disable=C0103
urlpatterns = patterns('',
    url(r'^testing/(?P<status>\d{3})/$', simulate_http_status),
    url(r'^$',
        list_detail.object_list,
        REQUEST_LOG_LIST_INFO,
        name="request_log_list"),
    url(r'^(?P<object_id>\d+)/$',
        list_detail.object_detail,
        REQUEST_LOG_DETAIL_INFO,
        name="request_log_object"),
)
