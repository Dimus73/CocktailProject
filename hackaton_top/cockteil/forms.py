from django import forms
from .models import *

class SetSearchForm(forms.Form):
    IngradientName = forms.CharField(max_length=50, label="Search string")
    categories     = forms.ModelChoiceField (queryset=IngredientsType.objects.all(), empty_label='choice')