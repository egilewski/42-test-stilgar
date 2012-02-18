import os
import errno
import shutil
import hashlib
from forty_two_test_stilgar import settings

def temporarily_store_image(uploaded_file, tmp_dir='tmp'):
    """Save uploaded file to tmp dir inside MEDIA_ROOT. Return tuple of
    id and path (relative to MEDIA_ROOT)."""
    relative_file_path = os.path.join(tmp_dir, uploaded_file.name)
    tmp_file_path = os.path.join(settings.MEDIA_ROOT, relative_file_path)
    try:
        os.makedirs(os.path.dirname(tmp_file_path))
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise
    with open(tmp_file_path, 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)
        f.close()

    image_id = hashlib.sha256(relative_file_path + settings.SECRET_KEY) \
            .hexdigest()
    return image_id, relative_file_path

def restore_stored_image(image_path, image_dir):
    filename = os.path.basename(image_path)
    old_path = os.path.join(settings.MEDIA_ROOT, image_path)
    new_path = os.path.join(image_dir, filename)
    shutil.move(old_path, os.path.join(settings.MEDIA_ROOT, new_path))
    return new_path

def drop_stored_image(request):
    try:
        os.remove(request.session[request.POST['image_preview_id']])
    except (KeyError, TypeError, OSError):
        pass
    try:
        del request.session[request.POST['image_preview_id']]
    except KeyError:
        pass
