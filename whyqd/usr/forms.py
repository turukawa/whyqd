from django import forms

from datetime import date

class SubscribeForm(forms.Form):
    subscribe_to = forms.DateField(label="Subscribe to", required=False, initial=date.today())

    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.fields['subscribe_to'].widget.attrs['class'] = 'datepicker'