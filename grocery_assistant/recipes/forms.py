from django.forms import ModelForm

from django import forms
from .models import Recipe


class RecipeForm(ModelForm):
    class Meta(object):
        model = Recipe
        fields = ['title', 'tags', 'ingredients', 'cooking_time', 'text',
                  'image', ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text', ]
