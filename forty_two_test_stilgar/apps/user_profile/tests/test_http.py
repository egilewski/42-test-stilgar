"""Webpage tests for user profile app."""
import re
import datetime
from django.utils.formats import date_format
from forty_two_test_stilgar.apps.user_profile.models import Profile
from forty_two_test_stilgar.helpers.test_helpers import HttpParsingTestCase


# pylint: disable=R0904
class TestUserProfileProfilePage(HttpParsingTestCase):
    """Tests user profile page."""
    xhtml = True

    def test_profile_page(self):
        """Asserts data from all fields (execpt for id) in model's object to be
        presented on page."""
        profile_data = Profile.objects.all()[0]
        self.go200('/')
        # Check all fields. If some field will be added and shouldn't be
        # outputed to the front page, it's OK for test to fail so it will be
        # obviuos that it needs to be changed.
        for field in profile_data.fields:
            if isinstance(field, datetime.date):
                field = date_format(field)
            self.find(field, flat=True, plain_text=True)
