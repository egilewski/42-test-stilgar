"""Request logger middleware."""
from forty_two_test_stilgar.apps.request_logger.models import Request


class RequestLoggerMiddleware(object):
    """Middleware that stores all HTTP requests in DB."""
    # pylint: disable=R0201,R0903
    def process_request(self, request):
        """Log HTTP request to database.
        Additionaly add information for testing if view
        "simulate_http_status" is about to be executed."""
        if request.path_info == '/favicon.ico':
            return

        log_data = {
                'path': request.path_info,
                'host': request.get_host(),
                'url': request.build_absolute_uri(),
                'method': request.method,
                'ip': request.META['REMOTE_ADDR'],
                'request': str(request),
            }
        try:
            log_data['user'] = request.user
            if log_data['user'].is_anonymous():
                log_data['user'] = None
        except AttributeError:
            log_data['user'] = None
        try:
            log_data['referer'] = request.META['HTTP_REFERER']
        except KeyError:
            log_data['referer'] = None
        # Demonstrational priority assignment.
        log_data['priority'] = self.get_request_priority(request)
        request_log = Request(**log_data)
        request_log.save()

        # Add request.log if it's call to special view for test case.
        request.log = log_data
        if request.path_info.startswith('request-log/testing'):
            request.log = log_data

    def get_request_priority(self, request):
        priority = 1
        if request.method == 'POST':
            priority += 10
        return priority
