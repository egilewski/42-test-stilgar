"""Request logger views. Request list and helper for tests
simulate_http_status(). Request detail view is in app's urlconf."""
from django.http import HttpResponse
import django.utils.simplejson as json
from django.views.generic.simple import direct_to_template
from forty_two_test_stilgar.apps.request_logger.models import Request


def request_list(request):
    """Show request list."""
    requests = Request.objects.order_by('id')[:10]
    requests = sorted(requests, key=lambda x: x.priority, reverse=True)
    return direct_to_template(request, template='request_logger_list.html',
                              extra_context={'request_record_list': requests})


def simulate_http_status(request, status):
    """Simulate requested http status."""
    serialized_request_log = json.dumps(request.log)
    return HttpResponse(serialized_request_log, status=int(status))
