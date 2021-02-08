import io
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import RecipeForm
from .models import Recipe, Tag
from .utils import generate_purchases_pdf

User = get_user_model()
TAGS = ['breakfast', 'lunch', 'dinner']

logger = logging.getLogger(__name__)


def index(request):
    """"
    Выводит список всех рецептов отсортированных по дате на главную страницу.
    """
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    recipe_list = Recipe.objects.filter(tags__title__in=tags).distinct()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    response = render(request, 'recipes/index.html', {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'all_tags': all_tags, }
                      )
    return response


def recipe_view(request, recipe_id):
    """
    Редирект на страницу с рецептом.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return redirect('slug_recipe_view', recipe_id=recipe.id, slug=recipe.slug)


def slug_recipe_view(request, recipe_id, slug):
    """
    Возвращает страницу рецепта по id и slug.
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


def profile_view(request, username):
    """
    Возвращает профайл пользователя с его рецептами.
    """
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()

    author = get_object_or_404(User, username=username)
    author_recipes = author.recipes.filter(
        tags__title__in=tags).prefetch_related('tags').distinct()

    paginator = Paginator(author_recipes, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/author_page.html',
        {
            'author': author,
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
        }
    )


class NewRecipe(LoginRequiredMixin, CreateView):
    """
    Создание нового рецепта.
    """
    form_class = RecipeForm
    template_name = 'recipes/form_recipe.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditRecipe(LoginRequiredMixin, UpdateView):
    """
    Изменение содержимого рецепта.
    """
    form_class = RecipeForm
    model = Recipe
    template_name = 'recipes/form_recipe.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        """
        Проверяем, что только автор рецепта может его изменить.
        """
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect(reverse('slug_recipe_view', kwargs={
                'slug': obj.slug, 'recipe_id': obj.id}))
        response = super(EditRecipe, self).dispatch(request, *args, **kwargs)
        return response


class DeleteRecipe(LoginRequiredMixin, DeleteView):
    """
    Удаление рецепта.
    """
    model = Recipe
    success_url = reverse_lazy('index')


@login_required
def favorites(request):
    """
    Возвращает список избранных рецептов.
    """
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    recipe_list = Recipe.objects.filter(favored_by__user=request.user,
                                        tags__title__in=tags).distinct()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    response = render(request, 'recipes/favorites.html',
                      {'page': page,
                       'paginator': paginator,
                       'tags': tags,
                       'all_tags': all_tags, }
                      )
    return response


@login_required
def subscriptions(request):
    """
    Возвращает список рецептов избранных авторов.
    """
    recipe_list = User.objects.filter(following__user=request.user)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    response = render(request, "recipes/follow.html",
                      {'page': page,
                       'paginator': paginator}
                      )
    return response


@login_required
def purchases(request):
    """
    Возвращает список покупок пользователя.
    """
    recipes = request.user.purchases.all()
    return render(request, 'recipes/purchases.html', {'recipes': recipes}, )


@login_required
def purchases_download(request):
    """
    Формирует pdf-файл со списком ингредиентов для покупки.
    """
    ingredients = request.user.purchases.select_related('recipe').order_by(
        'recipe__ingredients__title').values(
        'recipe__ingredients__title', 'recipe__ingredients__unit_measure'
    ).annotate(amount=Sum('recipe__ingredients_amounts__quantity')).all()

    pdf = generate_purchases_pdf('recipes/includes/purchases_list.html',
                                 {'ingredients': ingredients})

    return FileResponse(io.BytesIO(pdf), filename='ingredients.pdf',
                        as_attachment=True)


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
