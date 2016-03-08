from django import template
import collections

register = template.Library()


@register.filter
def get_value(dic, key):
    """get value from key"""

    return dic[str(key)]

@register.filter
def itemsort(dic):
    """sort set """
    return sorted(dic)

@register.filter
def dictsort(value):
    new_dict = collections.OrderedDict()
    key_list = sorted(value)
    for key in key_list:
        new_dict[key] = value[key]
    return new_dict