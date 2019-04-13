
from django import forms
from django.core.exceptions import ValidationError
from .models import Recipe


class RecipeForm(forms.ModelForm):
    name = forms.CharField(max_length=75, required=True)
    foodtype = forms.CharField(max_length=75, required=True)
    persons = forms.DecimalField(max_digits=2, decimal_places=0, required=True)
    link = forms.CharField(max_length=1000, required=True)
    class Meta:
        model = Recipe
        fields = ['name', 'foodtype', 'picture', 'persons', 'link']

    def clean_name(self):
        name = self.cleaned_data['name']
        name = name.title()
        return name

    def clean_price(self):
        persons = self.cleaned_data['persons']
        if persons < 1:
            raise ValidationError("Recipes must be at least for one person")

        return persons