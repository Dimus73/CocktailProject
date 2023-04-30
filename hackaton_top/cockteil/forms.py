from django import forms
from .models import *

class SetSearchForm(forms.Form):

    ingradient_name = forms.CharField(max_length=50, label="Search string", required=False)
    categories      = forms.ModelChoiceField (queryset=IngredientsType.objects.all().order_by('name'), empty_label='choice', required=False)
    only_bar        = forms.BooleanField(required=False)
    required_css_class = "form-label"
    def __init__(self, *args, **kwargs):
        super(SetSearchForm, self).__init__(*args, **kwargs)
        self.fields['ingradient_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['categories'].widget.attrs.update({'class': 'form-select'})
        self.fields['only_bar'].initial = False


class CocktailSerchNameForm (forms.Form):
    cocktail_part_name = forms.CharField(max_length=50, label="Search string", required=False)
    required_css_class = "form-label"

    def __init__(self, *args, **kwargs):
        super(CocktailSerchNameForm, self).__init__(*args, **kwargs)
        self.fields['cocktail_part_name'].widget.attrs.update({'class': 'form-control'})


class CocktailSerchIngradientForm (forms.Form):
    bar_list = Ownbar.objects.all().values_list('ingradient')
    ingr_list = Ingredients.objects.all().filter (pk__in=bar_list)

    ingradient         = forms.ModelChoiceField (queryset=ingr_list, label="Ingredient", empty_label='choice', required=False )
    required_css_class = "form-label55"

    def __init__(self, *args, **kwargs):
        super(CocktailSerchIngradientForm, self).__init__(*args, **kwargs)
        self.fields['ingradient'].widget.attrs.update({'class': 'form-select'})
