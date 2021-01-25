from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta(object):
        model = Recipe
        fields = ['title', 'tags', 'ingredients', 'cooking_time', 'text',
                  'image', ]

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text', ]
