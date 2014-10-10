from django import forms
from whyqd.novel.models import Novel, Token

class NovelForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ('title', 'pitch', )
        # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-fields
        widgets = {
            'pitch': forms.Textarea(attrs={'cols': 120, 'rows': 5}),
        }

class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ('recipient', )
        
    def __init__(self, *args, **kwargs):
        # http://pastebin.com/zZ0HDM1c
        super(TokenForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and not instance.is_valid:
            self.fields['recipient'].widget.attrs['readonly'] = True

# From https://github.com/fle/django-multi-email-field/

# From https://djangosnippets.org/snippets/1958/

import re

from django.core.validators import validate_email
from django.forms import CharField, Textarea, ValidationError

class EmailsListField(CharField):

    widget = Textarea

    def clean(self, value):
        super(EmailsListField, self).clean(value)
        emails = [item.strip() for item in re.compile(r'[,;]+').split(value) if item.strip()]
        if not emails:
            raise ValidationError(u'Enter at least one e-mail address.')
        for email in emails:
            validate_email(email)
        return emails
    
class BulkBuyForm(forms.Form):
    email_list = EmailsListField(label="Email list")