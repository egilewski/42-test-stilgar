"""Views for user profile app."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.user_profile.models import Profile


def user_profile(request):
    """Provides page with user profile information from Profile model."""
    profile = Profile.objects.all()[0]
    # Not using generic view, because this is simplier (ticket:1#comment:80).
    return render_to_response('user_profile_profile.html',
            {'profile': profile},
            context_instance=RequestContext(request))
