from django import forms


class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices = FEEDBACK_CHOICES)
from django.forms.widgets import RadioSelect
from .models import Book
class SearchForm(forms.Form):
    name = forms.CharField(required=False, label='Your Name')
    category = forms.ChoiceField(
        required=False,
        choices=Book.CATEGORY_CHOICES,
        label='Select a category:',
        widget=RadioSelect
    )
    max_price = forms.IntegerField(label='Maximum Price', min_value=0)

