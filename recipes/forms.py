from django import forms
from django.shortcuts import get_object_or_404

from decimal import Decimal

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeForm(forms.ModelForm):
    """
    Форма модели Recipe для добавления/удаления/изменения рецепта.
    """

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), to_field_name='title', )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(), to_field_name='title')

    # amount = []

    class Meta:
        model = Recipe
        fields = (
            'title', 'tags', 'ingredients', 'cooking_time', 'text', 'image',
        )
        widgets = {'tags': forms.CheckboxSelectMultiple(), }
        localized_fields = '__all__'

    # def __init__(self, data=None, *args, **kwargs):
    #     if data is not None:
    #         data = data.copy()
    #         print(data)
    #         ingredients = self.get_ingredients(data)
    #         for item in ingredients:
    #             data.update({"ingredients": item})
    #         self.amount = self.get_amount(data)
    #
    #     super().__init__(data=data, *args, **kwargs)

    def __init__(self, data=None, *args, **kwargs):  # v3
        if data is not None:
            data = data.copy()
            # print(data)
            self.recipe_ingredients = self.parse_ingredients(data)
            # print(self.recipe_ingredients)
            for item in self.recipe_ingredients:
                data.update({"ingredients": item})

        super().__init__(data=data, *args, **kwargs)

    def parse_ingredients(self, data):  # v3
        """
        Возвращает справочник: {название ингредиента ; количество}.
        """
        ingredients = {}
        for index, ingredient in data.items():
            if index.startswith('nameIngredient'):
                value = index.split('_')[1]
                ingredients[ingredient] = data[f'valueIngredient_{value}']
        return ingredients

    def save(self, commit=True):
        """
        Сохраняем сущность Рецепт с m2m связью
        """
        instance = forms.ModelForm.save(self, False)
        # instance = super().save(commit=False)
        instance.save()

        ingredients = self.recipe_ingredients

        instance.ingredients.clear()

        query = []
        for ingredient_name, value in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=ingredient_name)
            query.append(RecipeIngredient(
                recipe=instance,
                ingredient=ingredient,
                quantity=Decimal(value.replace(',', '.'))
            ))

        RecipeIngredient.objects.bulk_create(query)
        self.save_m2m()
        return instance

    # def get_ingredients(self, query_data):
    #     """Возвращает список с названием ингредиентов."""
    #     ingredients = [
    #         query_data[key]
    #         for key in query_data.keys()
    #         if key.startswith("nameIngredient")
    #     ]
    #     return ingredients
    #
    # def get_amount(self, q_dict):
    #     """Возвращает словарь ингредиент:количество."""
    #     result = {}
    #     for key in q_dict.keys():
    #         if key.startswith("nameIngredient"):
    #             n = key.split("_")[1]
    #             result[q_dict["nameIngredient_" + n]] = q_dict[
    #                 "valueIngredient_" + n
    #                 ]
    #     return result
