"""Request logger middleware."""
from forty_two_test_stilgar.apps.request_logger.models import Request
from forty_two_test_stilgar.apps.request_logger.views import \
        simulate_http_status


class RequestLoggerMiddleware(object):
    """Middleware that stores all HTTP requests in DB."""
    def process_request(self, request):
        """Log HTTP request to database.
        Additionaly add information for testing if view
        "simulate_http_status" is about to be executed."""
        log_data = {
                'path': request.path_info,
                'host': request.get_host(),
                'url': request.build_absolute_uri(),
                'method': request.method,
                'request': str(request),
            }
        try:
            log_data['user'] = request.user.id
        except AttributeError:
            log_data['user'] = None
        try:
            log_data['referer'] = request.META['HTTP_REFERER']
        except KeyError:
            log_data['referer'] = None
        request_log = Request(**log_data)
        request_log.save()

        # Add request.log if it's call to special view for test case.
        request.log = log_data
        if request.path_info.startswith('request-log/testing'):
            request.log = log_data
