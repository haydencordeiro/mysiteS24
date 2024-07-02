from django import forms


class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices = FEEDBACK_CHOICES)

class SearchForm(forms.Form):
    name = forms.CharField(required=False, label='Your Name')
    category = forms.ChoiceField(required=False, choices=[], label='Select a category:')
    max_price = forms.IntegerField(label='Maximum Price', min_value=0)

