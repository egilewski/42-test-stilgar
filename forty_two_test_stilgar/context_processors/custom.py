"""Custom context processors for 42-test-stilgar project."""
from django.contrib.sites.models import get_current_site


def site(request):
    """Context processor that provides variable "site" from
    "django.contrib.sites"."""
    site_data = get_current_site(request)
    return {'site': site_data}
