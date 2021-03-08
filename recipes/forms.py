from django import forms
from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, RecipeIngredient, Tag
from .utils import parse_ingredients


class RecipeForm(forms.ModelForm):
    """
    Форма модели Recipe для добавления/удаления/изменения рецепта.
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), to_field_name='title', )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(), to_field_name='title')

    class Meta:
        model = Recipe
        fields = (
            'title',
            'tags',
            'ingredients',
            'cooking_time',
            'text',
            'image',
        )
        widgets = {'tags': forms.CheckboxSelectMultiple(), }
        localized_fields = '__all__'

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            self.recipe_ingredients = parse_ingredients(data)
            for item in self.recipe_ingredients:
                data.update({'ingredients': item})

        super().__init__(data=data, *args, **kwargs)

    def save(self, commit=True):
        """
        Сохраняем сущность Рецепт с m2m связью.
        """
        instance = forms.ModelForm.save(self, False)
        instance.save()

        ingredients = self.recipe_ingredients
        instance.ingredients.clear()

        query = []
        for ingredient_name, value in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=ingredient_name)

            query.append(RecipeIngredient(
                recipe=instance,
                ingredient=ingredient,
                quantity=value,
            )
            )

        RecipeIngredient.objects.bulk_create(query)
        self.save_m2m()
        return instance
