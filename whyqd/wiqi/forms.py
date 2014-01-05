from django import forms
#https://docs.djangoproject.com/en/dev/topics/forms/modelforms/

from datetime import date
#from olwidget.forms import MapModelForm

from whyqd.wiqi.models import Wiqi, Text, Image, Book#, Geomap

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
        fields = ('is_live_from', 'is_live_to', 'is_protected', 'is_private', )

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('title', 'content', )
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )
        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'pitch', )
        # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-fields
        widgets = {
            'pitch': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }

class BookFullForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'authors', 'authorsort', 'pitch', 'cover_image', 'summary', 'language', 'series', 'series_index', 'ISBN', )
       
WIQI_FORM_TYPE_DICT = {
                       'text': TextForm,
                       'image': ImageForm,
                       'book': BookForm,
                       #'geomap': GeomapForm,
                       }

'''        
class GeomapForm(MapModelForm):
    class Meta:
        model = Geomap
        fields = ('name', 'map_shape', 'comment', )
'''