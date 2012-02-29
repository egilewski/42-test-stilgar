import os
import re
import Image
from django.template import Library
from forty_two_test_stilgar import settings

register = Library()


# http://djangosnippets.org/snippets/955/ modified for image path.
def thumbnail(filename, size='104x104'):
    """Generate on demand and save thumbnail for image path relative to
    MEDIA_ROOT directory."""
    try:
        absolute_filename = os.path.join(settings.MEDIA_ROOT, filename)
        # Defining the size.
        x, y = [int(x) for x in size.split('x')]
        # Defining the filename and the miniature filename.
        filehead, filetail = os.path.split(absolute_filename)
        basename, format = os.path.splitext(filetail)
        miniature = basename.decode('utf8') + '_' + size + format
        miniature_filename = os.path.join(filehead, miniature)
        miniature_url = filehead + '/' + miniature
        if os.path.exists(miniature_filename) and \
                os.path.getmtime(absolute_filename) > \
                os.path.getmtime(miniature_filename):
            os.unlink(miniature_filename)
        # If the image wasn't already resized, resize it.
        if not os.path.exists(miniature_filename):
            image = Image.open(absolute_filename)
            width, height = image.size
            # Already fits.
            if x > width and y > height:
                return filename
            # PIL can't write animated GIF.
            try:
                if image.format == 'GIF':
                    image.seek(1)
                    return filename
            except:
                pass
            image.thumbnail([x, y], Image.ANTIALIAS)
            try:
                image.save(miniature_filename, image.format, quality=90,
                           optimize=1)
            except:
                image.save(miniature_filename, image.format, quality=90)

        miniature_url = re.sub(r'^' + re.escape(settings.MEDIA_ROOT), '',
                               miniature_url, 1)
        return miniature_url
    except:
        return filename

register.filter(thumbnail)
