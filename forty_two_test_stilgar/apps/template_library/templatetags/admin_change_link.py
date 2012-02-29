from django.core.urlresolvers import reverse
from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag
def admin_change_link(token):
    try:
        content_type = ContentType.objects.get_for_model(token)
        app = content_type.app_label
        model = content_type.model
        url = reverse('admin:%s_%s_change' % (app, model), args=(token.id,))
    except:
        url = ''
    return url
