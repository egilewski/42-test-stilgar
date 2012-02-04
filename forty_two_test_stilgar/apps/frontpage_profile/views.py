from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Profile


def frontpage_profile(request):
    profile = Profile.objects.all()[0]
    return render_to_response('frontpage_profile_profile.html',
            {'profile': profile},
            context_instance=RequestContext(request))
