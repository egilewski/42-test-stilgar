"""Views for user profile app. Show data and edit data for staff."""
import os.path
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, user_passes_test
from forty_two_test_stilgar import settings
from forty_two_test_stilgar.helpers.image_preview import \
        temporarily_store_image, restore_stored_image, drop_stored_image
from forty_two_test_stilgar.apps.user_profile.models import Profile
from forty_two_test_stilgar.apps.user_profile.forms import ProfileEditForm


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
    extra_context = {}
    profile = Profile.objects.all()[0]
    if request.method == 'POST':
        image_preview_id = ''
        stored_image = None
        # Handle temporary soring image.
        if ('image' in request.FILES) or \
                (('forget_unsaved_image' in request.POST) and \
                request.POST['forget_unsaved_image']):
            drop_stored_image(request)
            request.POST['forget_unsaved_image'] = False
        if 'image' in request.FILES:
            if 'preview' in request.POST:
                image_id, image_path = temporarily_store_image(
                        request.FILES['image'])
                del request.FILES['image']
                extra_context['image_preview'] = image_path
                image_preview_id = image_id
                request.session[image_preview_id] = \
                        extra_context['image_preview']
                extra_context['unsaved_changes'] = True
        else:
            try:
                image_path = request.session[request.POST['image_preview_id']]
                extra_context['image_preview'] = image_path
                image_preview_id = request.POST['image_preview_id']
                stored_image = os.path.join(settings.MEDIA_ROOT,
                                            extra_context['image_preview'])
            except KeyError:
                pass
        request.POST['image_preview_id'] = image_preview_id

        # Handle action: preview or save.
        if 'preview' in request.POST:
            form = ProfileEditForm(request.POST, instance=profile)
            if form.has_changed():
                extra_context['unsaved_changes'] = True
            if ('image-clear' in request.POST) and \
                    request.POST['image-clear'] == 'on':
                extra_context['persistant_image_clear'] = \
                        request.POST['image-clear']
            extra_context['debug'] = request.POST
        elif 'save' in request.POST:
            form = ProfileEditForm(request.POST, request.FILES,
                                   instance=profile)
            if form.is_valid():
                if stored_image:
                    image_dir = profile.image.field.upload_to
                    stored_image = restore_stored_image(stored_image,
                                                        image_dir)
                form.save(stored_image=stored_image)
                # FIXME: rain dance.
                # Recreating form to update "Current value" of ImageField.
                form = ProfileEditForm(request.POST, instance=profile)
                drop_stored_image(request)
                extra_context = {}
    else:
        form = ProfileEditForm(instance=profile)
    extra_context['form'] = form
    return direct_to_template(request,
                             template='user_profile_edit.html',
                             extra_context=extra_context)
