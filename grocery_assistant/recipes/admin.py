from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     Subscription, Tag)

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Tag)
admin.site.register(Subscription)
admin.site.register(Favorite)
