from django import forms
from django.forms.widgets import RadioSelect
from .models import *

class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices = FEEDBACK_CHOICES)

class SearchForm(forms.Form):
    name = forms.CharField(required=False, label='Your Name')
    category = forms.ChoiceField(
        required=False,
        choices=Book.CATEGORY_CHOICES,
        label='Select a category:',
        widget=RadioSelect
    )
    max_price = forms.IntegerField(label='Maximum Price', min_value=0)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type':forms.RadioSelect}
        labels = {'member': u'Member name', }
