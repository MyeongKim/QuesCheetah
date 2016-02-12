from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def get_value(dic, key):
    """get value from key"""

    return dic[str(key)]

@register.filter
def itemsort(dic):
    """sort set """
    return sorted(dic)