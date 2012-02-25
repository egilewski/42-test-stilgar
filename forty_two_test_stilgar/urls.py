"""Django urlconf for forty_two_test_stilgar project."""
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from forty_two_test_stilgar import settings
from forty_two_test_stilgar.apps.user_profile.views import \
        user_profile, edit_user_profile

from django.contrib import admin
admin.autodiscover()

# pylint: disable=C0103
urlpatterns = patterns('',
    url(r'^$', user_profile, name='frontpage'),
    url(r'^edit-user-profile/$', edit_user_profile),
    url(r'^request-log/',
            include('forty_two_test_stilgar.apps.request_logger.urls')),
    url(r'^progress_file_input/',
            include('forty_two_test_stilgar.apps.progress_file_input.urls')),
    url(r'^accounts/login/$',  login, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
