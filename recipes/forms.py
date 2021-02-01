from django import forms
from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta(object):
        model = Recipe
        fields = ['title', 'tags', 'ingredients', 'cooking_time', 'text',
                  'image', ]
        widgets = {'tags': forms.CheckboxSelectMultiple(), }
