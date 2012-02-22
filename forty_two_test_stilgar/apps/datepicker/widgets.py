"""Widget for selecting dates with Jquery UI Datepicker."""
from django import forms
from django.utils.safestring import mark_safe
from forty_two_test_stilgar import settings


class DatePicker(forms.DateInput):
    """Widget for selecting dates with Jquery UI Datepicker."""
    # pylint: disable=W0232,R0903,C0111
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/' \
                    'jquery-ui.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/i18n/' \
                    'jquery-ui-i18n.min.js',
            'datepicker/widget.js',
        )
        css = {
            'all': (
                'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/' \
                        'smoothness/jquery-ui.css',
                'datepicker/datepicker.css',
            ),
        }

    def render(self, name, value, attrs=None):
        """Adding datepicker-needed identification and params for it."""
        attrs['data-datepicker-regional'] = settings.LANGUAGE_CODE
        attrs['data-datepicker-dateformat'] = 'yy-mm-dd'
        html = super(DatePicker, self).render(name, value, attrs)
        return mark_safe(html)
