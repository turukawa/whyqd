from django import template
from django.core.exceptions import ObjectDoesNotExist
#https://docs.python.org/3/library/collections.html#collections.OrderedDict
from collections import OrderedDict as SortedDict

register = template.Library()

@register.filter
def numdict(kwargs):
    """
    A method to handle a list of items in a dict with numeric keys
    :param kwargs:
    """
    dictlist = []
    for i in range(1, len(kwargs)+1):
        dictlist.append(kwargs[str(i)])
    return dictlist

@register.filter
def orderchapters(formset):
    """
    Returns an ordered set of chapters based on the position of the sentinal.
    :param formset:
    :return:
    """
    formsetlist = []
    formsetdict = {}
    sentinal = False
    for form in formset:
        formsetdict[form.instance.surl] = form
        try:
            form.instance.novel_sentinal
            sentinal = form.instance
            formsetlist.append(form)
        except ObjectDoesNotExist:
            pass
    if sentinal:
        while sentinal.next_wiqi:
            sentinal = sentinal.next_wiqi
            formsetlist.append(formsetdict[sentinal.surl])
        return formsetlist
    return formset

@register.filter(name='sort')
def listsort(value):
    if isinstance(value, dict):
        new_dict = SortedDict()
        key_list = sorted(value.keys())
        for key in key_list:
            new_dict[key] = value[key]
        return new_dict
    elif isinstance(value, list):
        value = sorted([(int(k), v) for (k, v) in value])
        return value
    else:
        return value
    listsort.is_safe = True