  
from django.template.defaulttags import register
from rebagApp.models import *

@register.filter
def get_dict_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_item(items, id):
    return Items.objects.get(id=id)

@register.filter()
def get_range(min=5):
    return range(1,int(min)+1)

    
@register.filter()
def total(cart):
    sum = 0
    for item in cart:
        sum += item.current_price
    return sum
    