"""ProgressFileInput urlconf. Only view for requesting upload progress."""
from django.conf.urls.defaults import patterns, url
from forty_two_test_stilgar.apps.progress_file_input.views import \
        upload_progress

# pylint: disable=C0103
urlpatterns = patterns('',
    url(r'^progress/$', upload_progress),
)
