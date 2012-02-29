"""Webpage tests for the request logger app."""
import datetime
from django.utils.formats import date_format
from twill.errors import TwillAssertionError
from BeautifulSoup import BeautifulSoup
from forty_two_test_stilgar.apps.request_logger.models import Request
from forty_two_test_stilgar.helpers.test_helpers import HttpParsingTestCase


# pylint: disable=R0904
class TestUserProfileProfilePage(HttpParsingTestCase):
    """Test logged uests list and details pages."""
    xhtml = True

    def test_request_list_page(self):
        """
        Assert data from all fields (execpt for "request" and
        "priority") in each of last 10 model's object to be presented
        on list view page.
        Assert other records not to be presented.
        """
        # Create enough request log entries.
        for i in xrange(20):
            self.go200('/request-log')
        self.check_presence(Request.objects.order_by('-id')[:10])
        self.assert_raises(TwillAssertionError,
                self.check_presence, Request.objects.order_by('-id')[10:20])

    def test_request_page(self):
        """Assert data from all fields (except "priority") in given
        model's object to be presented on detail view page."""
        # Visit page to ensure there is at least one log record.
        self.go200('/request-log/')
        request = Request.objects.order_by('-id')[0]
        self.go200('/request-log/' + str(request.id))
        fields = request.get_fields(exclude=('url', 'priority'))
        for value in fields.itervalues():
            if isinstance(value, datetime.datetime):
                value = date_format(value)
            if value is None:
                value = ''
            self.find(value, flat=True, plain_text=True)
        self.get_browser().find_link(request.url)

    def test_request_list_page_order(self):
        """Assert list to be ordered in decreasing of priority."""
        self.login_to_admin('admin', 'admin')
        # One log record.
        self.go200('/request-log')
        # Some page with form.
        self.go200('/admin/request_logger/request/1/')
        # One POST - it will have higer priority.
        self.submit200()
        # Newer record than POST - this must go after POST.
        self.go200('/request-log')
        soup = BeautifulSoup(self.get_browser().get_html().decode('UTF-8'))
        order_on_page = [int(''.join(td.a.contents)) \
                for td in soup.findAll('td', 'id')]
        last_priority = float('+inf')
        for i in order_on_page:
            request = Request.objects.get(pk=i)
            self.assert_true(request.priority <= last_priority)
            last_priority = request.priority

    def check_presence(self, request_list):
        for request in request_list:
            fields = request.get_fields(
                    exclude=('url', 'request', 'priority'))
            print fields
            for value in fields.itervalues():
                if isinstance(value, datetime.datetime):
                    value = date_format(value)
                if value is None:
                    value = ''
                self.find(value, flat=True, plain_text=True)
            self.assert_not_equal(self.get_browser().find_link(request.url),
                                  None)
