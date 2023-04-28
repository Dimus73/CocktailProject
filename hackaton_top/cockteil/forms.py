from django import forms
from .models import *

class SetSearchForm(forms.Form):
    ingradient_name = forms.CharField(max_length=50, label="Search string", required=False)
    categories     = forms.ModelChoiceField (queryset=IngredientsType.objects.all().order_by('name'), empty_label='choice', required=False)
    required_css_class = "form-label"
    def __init__(self, *args, **kwargs):
        super(SetSearchForm, self).__init__(*args, **kwargs)
        self.fields['ingradient_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['categories'].widget.attrs.update({'class': 'form-select'})


 