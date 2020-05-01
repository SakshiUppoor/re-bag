  
from django.template.defaulttags import register
from rebagApp.models import *

@register.filter
def get_dict_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_item(items, id):
    return Items.objects.get(id=id)