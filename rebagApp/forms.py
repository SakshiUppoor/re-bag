from django import forms
from .models import Item, Auction


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_description', 'base_price', 'category']


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['time', 'cap_time']
