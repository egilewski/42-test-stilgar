"""Webpage tests for user profile app."""
import re
import datetime
import os.path
from django.utils.formats import date_format
from BeautifulSoup import BeautifulSoup
from forty_two_test_stilgar.apps.user_profile.models import Profile
from forty_two_test_stilgar.helpers.test_helpers import HttpParsingTestCase


# pylint: disable=R0904,W0232
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
        for key, value in profile_data.fields.iteritems():
            if key == 'image' and value:
                self.find_url(value.url, flat=True)
            else:
                if isinstance(value, datetime.date):
                    value = date_format(value)
                self.find(value, flat=True, plain_text=True)

    def test_authorised_profile_edit(self):
        """Login, get and submit edit form and verify data in DB."""
        # Edit profile with authorisation.
        self.login('admin', 'admin')
        new_values = self.edit_profile()
        # Check DB.
        profile_data = Profile.objects.all()[0]
        for key, value in new_values.iteritems():
            profile_value = getattr(profile_data, key)
            if key == 'image':
                self.assert_true(
                        profile_value.name.endswith(os.path.basename(value)))
            else:
                if isinstance(profile_value, datetime.date):
                    value = datetime.datetime.strptime(value, '%Y-%m-%d') \
                            .date()
                else:
                    #FIXME: real errors regarding whitespace will be missed.
                    value = re.sub('((\r\n)|\r|\n)+', '\n', value.strip())
                    profile_value = re.sub('((\r\n)|\r|\n)+', '\n',
                            profile_value.strip())
                self.assert_equal(value, profile_value)
        # Check correspondence of DB and page after editing.
        self.test_profile_page()

    def test_unauthorised_profile_edit(self):
        """Verify unauthorised profile edit requests to be redirected to
        the login page."""
        self.go('/edit-user-profile/')
        self.find('<input type="hidden" name="this_is_the_login_form" ' \
                'value="1" />')

    def test_field_reversing(self):
        """Test if reversed order in columns are actually exact reversed
        comparing to normal."""
        self.login('admin', 'admin')

        # Get normal order.
        self.go('/edit-user-profile/')
        soup = BeautifulSoup(self.get_browser().get_html().decode('UTF-8'))
        first_column = soup.find(attrs={'id': 'field-column-1'})
        first_column_normal_order = [field['id'] for field in \
                first_column.findAll(attrs='field-wrapper')]
        second_column = soup.find(attrs={'id': 'field-column-2'})
        second_column_normal_order = [field['id'] for field in \
                second_column.findAll(attrs='field-wrapper')]

        # Get reversed order.
        self.go('/edit-user-profile/?reverse_field_order=1')
        soup = BeautifulSoup(self.get_browser().get_html().decode('UTF-8'))
        first_column = soup.find(attrs={'id': 'field-column-1'})
        first_column_reversed_order = [field['id'] for field in \
                first_column.findAll(attrs='field-wrapper')]
        second_column = soup.find(attrs={'id': 'field-column-2'})
        second_column_reversed_order = [field['id'] for field in \
                second_column.findAll(attrs='field-wrapper')]

        # Compare orders.
        self.assert_equal(first_column_normal_order,
                     list(reversed(first_column_reversed_order)))
        self.assert_equal(second_column_normal_order,
                     list(reversed(second_column_reversed_order)))

    def edit_profile(self):
        """Perform profile editing and check for success."""
        form_id = 1
        self.go200('/edit-user-profile/')
        new_values = {
            'first_name': 'Test First Name',
            'last_name': 'Test Last Name',
            'date_of_birth': '2012-01-01',
            'bio': 'Test bio\r\n',
            'email': 'test@example.com',
            'jabber': 'test2@example.com',
            'skype': 'testskype',
            'contacts': 'Test \n contacts',
            'image': os.path.abspath(os.path.dirname(__file__)) + \
                    '/testimage.jpg'
        }
        for key, value in new_values.iteritems():
            if key != 'image':
                self.formvalue(form_id, key, value)
            else:
                self.formfile(form_id, key, value)
        self.submit200('preview')
        self.find('<img[^>]*' + os.path.basename(new_values['image']))
        self.submit200('save')
        self.notfind('<p class="errornote">')
        return new_values
