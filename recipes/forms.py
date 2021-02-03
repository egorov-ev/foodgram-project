from django import forms
from django.forms import ModelForm

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeForm(ModelForm):
    """
    Форма модели Recipe для добавления/удаления/изменения рецепта.
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), to_field_name="title", )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(), to_field_name="title"
    )
    amount = []

    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'ingredients', 'cooking_time', 'text',
                  'image',)
        widgets = {'tags': forms.CheckboxSelectMultiple(), }

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            print(data)
            ingredients = self.get_ingredients(data)
            print(ingredients)
            for item in ingredients:
                data.update({"ingredients": item})
            self.amount = self.get_amount(data)

        super().__init__(data=data, *args, **kwargs)

    def save(self, commit=True):
        recipe_obj = super().save(commit=False)
        recipe_obj.save()
        ingredients_amount = self.amount
        recipe_obj.RecipeIngredient_set.all().delete()
        recipe_obj.RecipeIngredient_set.set([RecipeIngredient(
            recipe=recipe_obj,
            ingredient=ingredient,
            quantity=ingredients_amount[ingredient.title], )
            for ingredient in self.cleaned_data["ingredients"]],
            bulk=False, )
        self.save_m2m()
        return recipe_obj

    def get_ingredients(self, query_data):
        """
        Возвращает список с названием ингредиентов
        """
        ingredients = [query_data[key]
                       for key in query_data.keys()
                       if key.startswith("nameIngredient")]
        return ingredients

    def get_amount(self, q_dict):
        """
        Возвращает словарь ингредиент:количество
        """
        result = {}
        for key in q_dict.keys():
            if key.startswith("nameIngredient"):
                n = key.split("_")[1]
                result[q_dict["nameIngredient_" + n]] = q_dict[
                    "valueIngredient_" + n]
        return result
