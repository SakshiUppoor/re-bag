from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from .models import Item, Auction
from django.forms import ModelForm, DateTimeInput
from django.contrib.admin import widgets
from django.forms import MultiWidget
from django.contrib.auth import get_user_model

User = get_user_model()

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

class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        label = 'First name',
        max_length = 1000,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'bor8 bg0 m-b-12 stext-111 cl8 plh3 size-111 p-lr-15'}
        )
    )
    last_name = forms.CharField(
        label = 'Last name',
        max_length = 1000,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'bor8 bg0 m-b-12 stext-111 cl8 plh3 size-111 p-lr-15'}
        )
    )
    email = forms.EmailField(
        label = 'Body',
        max_length = 1000,
        required = True,
        widget = forms.EmailInput(
            attrs = {'class': 'bor8 bg0 m-b-12 stext-111 cl8 plh3 size-111 p-lr-15'}
        )
    )
    phone = forms.CharField(
        label = 'Body',
        max_length = 1000,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'bor8 bg0 m-b-12 stext-111 cl8 plh3 size-111 p-lr-15'}
        )
    )
    address = forms.CharField(
        label = 'Adress',
        max_length = 1000,
        required = True,
        widget = forms.Textarea(
            attrs = {'class': 'bor8 bg0 m-b-12 stext-111 cl8 plh3 size-111 p-lr-15'}
        )
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address','image']