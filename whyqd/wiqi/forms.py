from django import forms
from django.forms.models import modelformset_factory
#https://docs.djangoproject.com/en/dev/topics/forms/modelforms/

from datetime import date
#from olwidget.forms import MapModelForm

from whyqd.wiqi.models import Wiqi, Text, Image #, Book#, Geomap

class WiqiStackRevertForm(forms.Form):
    comment = forms.CharField(max_length=500, required=False, label="Reason for reversion")

class WiqiStackRangeForm(forms.Form):
    range_from = forms.DateField(label="from", required=False)
    range_to = forms.DateField(label="to", required=False, initial=date.today())
    
    def __init__(self, *args, **kwargs):
        super(WiqiStackRangeForm, self).__init__(*args, **kwargs)
        self.fields['range_from'].widget.attrs['class'] = 'datepicker'
        self.fields['range_to'].widget.attrs['class'] = 'datepicker'

class WiqiForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WiqiForm, self).__init__(*args, **kwargs)
        self.fields['is_live_from'].widget.attrs['class'] = 'datepicker'
        self.fields['is_live_to'].widget.attrs['class'] = 'datepicker'

    class Meta:
        model = Wiqi
        fields = ('is_live_from', 'is_live_to', 'is_private', )

class WiqiPriceForm(forms.ModelForm):
    class Meta:
        model = Wiqi
        fields = ('price', 'read_if',)

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('title', 'content', )
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )


# class BookFullForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ('title', 'authors', 'authorsort', 'pitch', 'cover_image', 'summary', 'language', 'series', 'series_index', 'ISBN', )
       
WIQI_FORM_TYPE_DICT = {
                       'text': TextForm,
                       'image': ImageForm,
                       #'book': BookForm,
                       #'geomap': GeomapForm,
                       }

'''        
class GeomapForm(MapModelForm):
    class Meta:
        model = Geomap
        fields = ('name', 'map_shape', 'comment', )


# Dynamic Form Generation - http://jacobian.org/writing/dynamic-form-generation/
# Django passing object ID in hiddeninput by populating - http://stackoverflow.com/q/16668463
# https://docs.djangoproject.com/en/dev/topics/forms/formsets/
# Multi-Object-Edit With Django FormSets - http://christiankaula.com/multi-object-edit-django-formsets.html
'''