from django.contrib import admin
from django.db.models import Count

from .models import Comment, Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 0
    verbose_name = 'ингредиент'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = (
        'id', 'pub_date', 'title', 'author', 'slug',
        'cooking_time', 'get_favorite_count'
    )
    list_filter = ('author', 'tags__title')
    search_fields = ('title', 'author__username')
    autocomplete_fields = ('author',)
    ordering = ('-pub_date',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(favorite_count=Count('favored_by'))

    def get_favorite_count(self, obj):
        return obj.favorite_count


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
