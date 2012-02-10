"""Database tests for the request logger app."""
from tddspry.django import DatabaseTestCase
from tddspry.django.settings import SITE
import twill
import django.utils.simplejson as json
from forty_two_test_stilgar.apps.request_logger.models import Request


# pylint: disable=R0904
class TestRequestLoggerLog(DatabaseTestCase):
    """Test Request Logger model's data."""
    def test_request_logger_request_saved(self):
        """Simulates request of front page and then asserts that there is one
        and only one Request model objects."""
        log_entries = Request.objects.count()
        for code in 200, 403, 404, 500:
            twill.commands.go(SITE + 'request-log/testing/' + str(code))
            http_return = twill.commands.get_browser().get_html()
            log_entries += 1
            # Assert added records count.
            self.assert_count(Request, log_entries)
            # Assert saved data.
            log = json.loads(http_return)
            self.assert_read(Request, **log)
