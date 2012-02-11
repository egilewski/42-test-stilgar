"""https://code.djangoproject.com/browser/django/trunk/django/template/defaultfilters.py"""
from django import template
from forty_two_test_stilgar.apps.template_library.text_utils import Truncator

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def truncatechars(value, arg):
    """
    Truncates a string after a certain number of characters.

    Argument: Number of characters to truncate after.
    """
    try:
        length = int(arg)
    except ValueError: # Invalid literal for int().
        return value # Fail silently.
    return Truncator(value).chars(length)
truncatechars.is_safe=True
