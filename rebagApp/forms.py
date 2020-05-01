from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from .models import Item, Auction
from django.forms import ModelForm, DateTimeInput
from django.contrib.admin import widgets
from django.forms import MultiWidget


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_description', 'base_price', 'category', 'condition']

#     # ...

class AuctionForm(forms.ModelForm):
    start = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            })
    )
    cap_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            })
    )

    class Meta:
        model = Auction
        fields = ['start', 'cap_time']
