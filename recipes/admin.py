from django.contrib import admin

from .models import Comment, Ingredient, Recipe, RecipeIngredient, Tag


class IngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientsInline, ]
    list_display = (
        'id', 'pub_date', 'title', 'author', 'slug',
        'cooking_time',)
    list_filter = ('author', 'tags__title')
    search_fields = ('title', 'author__username')
    ordering = ('-pub_date',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'unit_measure')
    search_fields = ('^title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'color', 'display_name')
    list_filter = ('title',)


@admin.register(RecipeIngredient)
class RecipeIngredient(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'quantity')
    list_filter = ('recipe',)


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('pk', 'post', 'author', 'text', 'comment_pub_date',)
    list_filter = ('post', 'author', 'comment_pub_date')
