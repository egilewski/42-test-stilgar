from tddspry.django import DatabaseTestCase
from tddspry.django import HttpTestCase
from twill.errors import TwillAssertionError
# FIXME: delete prefix, fix django-nose to work without it.
from forty_two_test_stilgar.apps.frontpage_profile.models import Profile
from forty_two_test_stilgar.apps.frontpage_profile.helpers \
        import format_date_of_birth

class TestFrontPageProfileDB(DatabaseTestCase):
    def test_front_page(self):
        self.assert_count(Profile, 1)

class TestFrontPageProfileHTTP(HttpTestCase):
    def test_front_page(self):
        # Get data from DB that must be rendered on front page.
        profile_data = Profile.objects.all()[0]
        # Check if all required data is present on web page.
        self.go200('/')
        for field in profile_data._meta.fields:
            if field.column == 'id':
                continue
            value = getattr(profile_data, field.column)
            if field.column == 'date_of_birth':
                value = format_date_of_birth(value)
            self.find(value)
