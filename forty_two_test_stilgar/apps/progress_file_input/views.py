"""ProgressFileInput view for AJAX requests. Returns upload progress
for given X-Progress-ID.
Source: http://djangosnippets.org/snippets/678/"""

from django.http import HttpResponse, HttpResponseServerError
from django.core.cache import cache
from django.utils import simplejson

def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = None
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key, {'state': 'starting'})
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseServerError('Server Error: You must provide' \
                ' X-Progress-ID header or query param.')
