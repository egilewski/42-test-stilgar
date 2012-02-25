"""ProgressFileInput file upload widget with progress bar upder file field."""
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from forty_two_test_stilgar import settings
from forty_two_test_stilgar.apps.progress_file_input.views import \
        upload_progress

class ProgressFileInput(forms.ClearableFileInput):
    """Widget for showing file upload progress."""
    render_template = u'''
            <div class="progress-file-input">
                <div %(hide_current)s class="current-value">
                    %(initial_text)s: %(initial)s %(clear_template)s
                </div>
                %(input_text)s: <span class="input-wrapper">%(input)s</span>
                <div
                    style="display: none;"
                    class="upload-progress"
                    id="%(container_id)s"
                    data-jquery-path="%(jquery-path)s"
                    data-upload-progress-path="%(upload-progress-path)s"
                    data-progress-url="%(progress-url)s"
                >
                    <div class="bar" id="%(bar_id)s"></div>
                    <div class="status"></div>
                </div>
            </div>
            '''


    # pylint: disable=W0232,R0903,C0111
    class Media:
        jquery_url = 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/' \
                'jquery.min.js'
        jquery_upload_progress_url = 'progress_file_input/jquery.uploadProgress.js'

        js = (
            jquery_url,
            jquery_upload_progress_url,
            'progress_file_input/progress_file_input.js',
        )

    def render(self, name, value, attrs=None):
        # FIXME: contains copy of parent's method, calls grandparent's method.
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
            'input': super(forms.ClearableFileInput, self).render(name, value,
                                                                  attrs),

            'container_id': 'upload-progress-' + name,
            'bar_id': 'upload-progress-%s-bar' % name,
            'jquery-path': self.Media.jquery_url,
            'upload-progress-path': settings.STATIC_URL + \
                    self.Media.jquery_upload_progress_url,
            'progress-url': reverse(upload_progress),
        }

        if value and hasattr(value, "url"):
            substitutions['hide_current'] = u''
            substitutions['initial'] = u'<a href="%s">%s</a>' % \
                    (escape(value.url), escape(force_unicode(value)))
        else:
            substitutions['hide_current'] = u'style="display: none;"'
            substitutions['initial'] = u'<a href=""></a>'

        template = self.render_template

        if not self.is_required:
            checkbox_name = self.clear_checkbox_name(name)
            checkbox_id = self.clear_checkbox_id(checkbox_name)
            substitutions['clear_checkbox_name'] = \
                    conditional_escape(checkbox_name)
            substitutions['clear_checkbox_id'] = \
                    conditional_escape(checkbox_id)
            substitutions['clear'] = \
                    forms.CheckboxInput().render(checkbox_name, False,
                                           attrs={'id': checkbox_id})
            substitutions['clear_template'] = \
                    self.template_with_clear % substitutions

        return mark_safe(template % substitutions)



        substitutions = {
        }

        return mark_safe(self.render_template % substitutions)
