"""Tests for context processor that adds Django settings to the context."""
from tddspry import NoseTestCase
from forty_two_test_stilgar import settings
from forty_two_test_stilgar.context_processors.django_settings import \
        django_settings


class DjangoSettingsTestCase(NoseTestCase):
    def test_context_processor(self):
        try:
            # This context processor doesn't need HttpRequest.
            context_settings = django_settings(None)['django_settings']
        except KeyError:
            raise Exception('Context variable "django_settings" isn\'t' \
                    ' provided.')
        current_settings = settings.__dict__
        try:
            for key in current_settings:
                if not key.startswith('__'):
                    self.assert_equal(
                            current_settings[key],
                            context_settings[key],
                            'Setting %s in template context not equals' \
                                    ' actual settings.' % key)
        except KeyError:
            raise Exception('Context variable "django_settings" lacks' \
                    ' attribute %s.' % key)
