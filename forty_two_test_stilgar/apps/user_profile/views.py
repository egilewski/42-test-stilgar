"""Views for user profile app. Show data and edit data for staff."""
import os.path
from django.utils import simplejson
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.encoding import force_unicode
from django.utils.translation import ungettext
from forty_two_test_stilgar import settings
from forty_two_test_stilgar.helpers.image_preview import \
        temporarily_store_image, restore_stored_image, drop_stored_image
from forty_two_test_stilgar.apps.user_profile.models import Profile
from forty_two_test_stilgar.apps.user_profile.forms import ProfileEditForm
from forty_two_test_stilgar.apps.template_library.templatetags import \
        simple_thumbnail


def user_profile(request):
    """Page with user profile information from Profile model."""
    profile = Profile.objects.all()[0]
    # Not using object_detail generic view, because this is simpler -
    # see (ticket:1#comment:80).
    return direct_to_template(request,
                             template='user_profile_profile.html',
                             extra_context={'profile': profile})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user_profile(request):
    """User profile edit page."""
    #TODO: make this view short.
    profile = Profile.objects.all()[0]
    reverse_field_order = ('reverse_field_order' in request.GET) and \
            request.GET['reverse_field_order'] == '1'
    default_extra_context = {'reverse_field_order': reverse_field_order}
    extra_context = default_extra_context

    if request.method == 'POST':
        # Handle temporary storing image.
        stored_image = None
        if 'forget_unsaved_image' in request.POST:
            forget_unsaved_image = request.POST['forget_unsaved_image']
            request.POST['forget_unsaved_image'] = False
        else:
            forget_unsaved_image = False
        if ('image' in request.FILES) or forget_unsaved_image:
            drop_stored_image(request)
        image_preview_id = ''
        if 'image' in request.FILES:
            if 'preview' in request.POST:
                image_id, image_path = temporarily_store_image(
                        request.FILES['image'])
                del request.FILES['image']
                extra_context['image_preview'] = image_path
                image_preview_id = image_id
                request.session[image_preview_id] = \
                        extra_context['image_preview']
        else:
            if request.POST['image_preview_id'] in request.session:
                image_path = request.session[request.POST['image_preview_id']]
                image_preview_id = request.POST['image_preview_id']
                stored_image = os.path.join(settings.MEDIA_ROOT, image_path)
                if 'preview' in request.POST:
                    extra_context['image_preview'] = image_path
        request.POST['image_preview_id'] = image_preview_id

        # Thumbnail.
        if 'image_preview' in extra_context:
            extra_context['image_preview'] = simple_thumbnail.thumbnail(
                    extra_context['image_preview'], '600x500')

        # Handle action: preview or save.
        if 'preview' in request.POST:
            form = ProfileEditForm(request.POST, instance=profile,
                                   reverse_field_order=reverse_field_order)
            if ('image-clear' in request.POST) and \
                    request.POST['image-clear'] == 'on':
                extra_context['persistent_image_clear'] = \
                        request.POST['image-clear']
        elif 'save' in request.POST:
            form = ProfileEditForm(request.POST, request.FILES,
                                   instance=profile,
                                   reverse_field_order=reverse_field_order)
            if form.is_valid():
                if stored_image:
                    image_dir = profile.image.field.upload_to
                    stored_image = restore_stored_image(stored_image,
                                                        image_dir)
                form.save(stored_image=stored_image)
                # FIXME: rain dance.
                # Recreating form to update "Current value" of ImageField.
                profile = Profile.objects.get(id=profile.id)
                form = ProfileEditForm(request.POST, instance=profile,
                                       reverse_field_order=reverse_field_order)
                drop_stored_image(request)
                extra_context = default_extra_context
    else:
        form = ProfileEditForm(instance=profile,
                               reverse_field_order=reverse_field_order)

    if form.is_bound and not form.is_valid():
        # Show errors.
        extra_context['error_note'] = ungettext(
                'Please correct the error below.',
                'Please correct the errors below.',
                len(form.errors))
        extra_context['form_errors'] = form.errors

    if request.is_ajax():
        if 'image_preview_id' in request.POST:
            extra_context['image_preview_id'] = \
                    request.POST['image_preview_id']
        if 'image_preview' in extra_context:
            extra_context['image_preview'] = \
                    settings.MEDIA_URL + extra_context['image_preview']
        if forget_unsaved_image and ('image_preview' in extra_context):
            del extra_context['image_preview']
        # "Current" in ClearableFileInput.
        if (profile.image):
            extra_context['current_image_url'] = profile.image.url
            extra_context['current_image_name'] = force_unicode(profile.image)
        else:
            extra_context['current_image_url'] = ''
            extra_context['current_image_name'] = ''

        return HttpResponse(simplejson.dumps(extra_context),
                            mimetype="application/json")
    else:
        extra_context['form'] = form
        return direct_to_template(request,
                                  template='user_profile_edit.html',
                                  extra_context=extra_context)
