"""Context processor for adding Django settings to the context."""
from copy import copy
from forty_two_test_stilgar import settings

def django_settings(request):
    """Context processor for adding "django_settings" to the context."""
    django_settings = copy(settings.__dict__)
    for key in django_settings.keys():
        if key.startswith('__'):
            del django_settings[key]
    return {'django_settings': django_settings}
