from django.core.urlresolvers import reverse, NoReverseMatch
from django import template

register = template.Library()


@register.simple_tag
def admin_change_link(token):
    try:
        app = token._meta.app_label
        model = token._meta.module_name
        url = reverse('admin:%s_%s_change' % (app, model), args=(token.id,))
    except:
        url = ''
    return url
