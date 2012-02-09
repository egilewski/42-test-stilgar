"""Database tests for user profile app."""
from tddspry.django import DatabaseTestCase
from forty_two_test_stilgar.apps.user_profile.models import Profile


# pylint: disable=R0904
class TestUserProfileProfileModel(DatabaseTestCase):
    """Tests Profile model's data."""
    def test_profile_model_valid_data(self):
        """Asserts that there is one and only one Profile model objects."""
        self.assert_count(Profile, 1)
