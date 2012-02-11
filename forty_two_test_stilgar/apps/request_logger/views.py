"""Request logger views. Helper for tests simulate_http_status(). Request
lists are in app's urlconf."""
from django.http import HttpResponse
import django.utils.simplejson as json


def simulate_http_status(request, status):
    """Simulate requested http status."""
    serialized_request_log = json.dumps(request.log)
    return HttpResponse(serialized_request_log, status=int(status))
