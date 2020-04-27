from django import forms
from .models import Item, Auction
from django.forms import ModelForm, DateTimeInput
from django.contrib.admin import widgets
from django.forms import MultiWidget
from bootstrap_datepicker_plus import DatePickerInput


# class ItemForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields = ['item_name', 'item_description', 'base_price', 'cat']

# class DateInput(forms.DateInput):
#     input_type = 'date'

# class SplitDateTimeWidget(MultiWidget):

#     # ...

#     def decompress(self, value):
#         if value:
#             return [value.date(), value.time()]
#         return [None, None]

class AuctionForm(ModelForm):
    class Meta:
    	start = forms.DateTimeField(input_formats=('%Y-%m-%dT%H:%M'))
    	cap = forms.DateTimeField(input_formats=('%Y-%m-%dT%H:%M'))
    	model = Auction
    	fields = ['start', 'cap']
        # widgets = {
        # 	'start': DateTimeInput()
        # }
        # widgets = {
        #     'date': DateTimeInput(attrs={'type': 'datetime-local'}),
        # }
        
    # def __init__(self, *args, **kwargs):
    #     super(AuctionForm, self).__init__(*args, **kwargs)
    #     self.fields['start'].widget = widgets.AdminSplitDateTime()
    #     self.fields['cap'].widget = widgets.AdminSplitDateTime()

class ProductForm(ModelForm):
	class Meta:
		model= Item
		fields=['item_name','item_description','condition','base_price','cat']