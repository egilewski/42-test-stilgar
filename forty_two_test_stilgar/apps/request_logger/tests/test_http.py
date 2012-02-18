"""Webpage tests for the request logger app."""
import datetime
from django.utils.formats import date_format
from forty_two_test_stilgar.apps.request_logger.models import Request
from forty_two_test_stilgar.helpers.test_helpers import HttpParsingTestCase


# pylint: disable=R0904
class TestUserProfileProfilePage(HttpParsingTestCase):
    """Test logged requests list and details pages."""
    xhtml = True

    def test_requests_page(self):
        """Assert data from all fields (execpt for "request") in each of
        last 10 model's object to be presented on list view page."""
        self.go200('/request-log')
        for request in Request.objects.order_by('-id')[0:10]:
            fields = request.get_fields(exclude=('url', 'request'))
            for value in fields.itervalues():
                if isinstance(value, datetime.datetime):
                    value = date_format(value)
                if value is None:
                    value = ''
                self.find(value, flat=True, plain_text=True)
            self.get_browser().find_link(request.url)

    def test_request_page(self):
        """Assert data from all fields in each of last model's object
        to be presented on detail view page."""
        # Visit page to ensure there is at least one log record.
        self.go200('/request-log/')
        request = Request.objects.order_by('-id')[0]
        self.go200('/request-log/' + str(request.id))
        print request.get_fields(exclude=('url',))
        fields = request.get_fields(exclude=('url', 'request'))
        for value in fields.itervalues():
            if isinstance(value, datetime.datetime):
                value = date_format(value)
            if value is None:
                value = ''
            self.find(value, flat=True, plain_text=True)
        self.get_browser().find_link(request.url)
