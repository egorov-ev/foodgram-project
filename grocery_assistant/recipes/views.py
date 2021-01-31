from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, UpdateView

import pdfkit

from decimal import Decimal

from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from .forms import RecipeForm
from .models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()
TAGS = ['breakfast', 'lunch', 'dinner']


# @cache_page(20, key_prefix="index_page")
# @login_required TODO главная отличается для авторизовнных и не авторизованных
def index(request):
    """"
    TODO добавить описание
    """
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()

    # recipe_list = Recipe.objects.select_related().all()
    recipe_list = Recipe.objects.filter(tags__title__in=tags).select_related(
        'author').prefetch_related('tags').distinct()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    response = render(
        request,
        'recipes/index.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
        }

    )
    return response


def subscriptions(request):
    """
    Возвращает список рецептов избранных авторов.
    """
    # recipe_list = Recipe.objects.filter(author__following__user=request.user)
    recipe_list = User.objects.filter(
        following__user=request.user).prefetch_related('recipes').annotate(
        recipe_count=Count('recipes')).order_by('username')
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    response = render(request,
                      "recipes/follow.html",
                      {
                          'page': page,
                          'paginator': paginator
                      }
                      )
    return response


def favorites(request):
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()

    # recipe_list = Recipe.objects.filter(tags__title__in=tags).select_related(
    #     'author').prefetch_related('tags').distinct()

    recipe_list = Recipe.objects.filter(favored_by__user=request.user,
                                        tags__title__in=tags).select_related(
        'author').prefetch_related('tags').distinct()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    response = render(request,
                      "recipes/favorites.html",
                      {
                          'page': page,
                          'paginator': paginator
                      }
                      )
    return response


def purchases(request):
    pass
    return None


# class NewRecipe(CreateView):
#     """
#     Создаем новый рецепт.
#     """
#     form_class = RecipeForm
#     template_name = "recipes/formRecipe.html"
#     success_url = reverse_lazy("index")
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         response = super(NewRecipe, self).form_valid(form)
#         return response

def get_ingredients(request):
    """
    Parse POST request body for ingredient names and their respective amounts.
    """
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]

    return ingredients


def save_recipe(request, form):
    """
    Create and save a Recipe instance with neccessary m2m relationships.
    """
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            objs = []
            ingredients = get_ingredients(request)
            for name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=name)
                objs.append(
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=Decimal(quantity.replace(',', '.'))
                    )
                )
            RecipeIngredient.objects.bulk_create(objs)

            form.save_m2m()
            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest


def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)

        return redirect(
            'slug_recipe_view', recipe_id=recipe.id, slug=recipe.slug
        )

    return render(request, 'recipes/formRecipe.html', {'form': form})


class EditRecipe(UpdateView):
    """
    Изменяем содержимое рецепта.
    """
    model = Recipe
    template_name = 'recipes/formRecipe.html'
    fields = ['title', 'tags', 'ingredients',
              'cooking_time', 'text', 'image', ]

    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     """
    #     Проверяем, что только автор поста может его изменить.
    #     """
    #     obj = self.get_object()
    #     if obj.author != self.request.user:
    #         return redirect(
    #             reverse('index', kwargs={
    #                 'username': obj.author,
    #                 'recipe_id': obj.id})
    #         )
    #     response = super(EditRecipe, self).dispatch(request, *args, **kwargs)
    #     return response

    # def get_context_data(self, **kwargs):
    #     """
    #     Изменяем шаблон в зависимости сценария.
    #     """
    #     context = super().get_context_data(**kwargs)
    #     context['source'] = True
    #     return context


class DeleteRecipe(DeleteView):
    """
    Удаляем рецепт.
    """
    model = Recipe
    success_url = reverse_lazy('index')

    # добавить в шаблон recipe.html {% url 'delete_recipe' author.get_username recipe.id %}


def profile_view(request, username):
    """
    Возвращает страницу автора и его посты.
    """
    author = get_object_or_404(User, username=username)
    recipes = author.recipes.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    response = render(request,
                      'recipes/author_page.html',
                      {
                          'author': author,
                          'page': page,
                          'paginator': paginator,
                      }
                      )
    return response


def recipe_view(request, recipe_id):
    """
    TODO сделать возможность комментировать рецепты
    Редирект на страницу с рецептом
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return redirect('slug_recipe_view', recipe_id=recipe.id, slug=recipe.slug)


def slug_recipe_view(request, recipe_id, slug):
    """
    Возвращает страницу рецепта по id и slug
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id, slug=slug)
    response = render(request,
                      'recipes/recipe_page.html',
                      {
                          "author": recipe.author,
                          "recipe": recipe,
                      }
                      )
    return response


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
