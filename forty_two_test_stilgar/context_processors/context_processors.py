from django.contrib.sites.models import get_current_site


def site_context_processor(request):
    """Context processor that provides variable ``site`` from
    ``django.contrib.sites``."""

    site = get_current_site(request)
    return {'site': site}
