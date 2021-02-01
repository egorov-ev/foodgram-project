import io

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.edit import ModelFormMixin

from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Tag
from .utils import generate_pdf

User = get_user_model()
TAGS = ['breakfast', 'lunch', 'dinner']


def index(request):
    """"
    TODO добавить описание
    """
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
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


@login_required
def subscriptions(request):
    """
    Возвращает список рецептов избранных авторов.
    """
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


@login_required
def favorites(request):
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    recipe_list = Recipe.objects.filter(favored_by__user=request.user,
                                        tags__title__in=tags).select_related(
        'author').prefetch_related('tags').distinct()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    response = render(request, 'recipes/favorites.html',
                      {
                          'page': page,
                          'paginator': paginator,
                          'tags': tags,
                          'all_tags': all_tags,
                      }
                      )
    return response


@login_required
def purchases(request):
    """
    TBD
    """
    recipes = request.user.purchases.all()
    return render(
        request,
        'recipes/purchases.html',
        {'recipes': recipes},
    )


@method_decorator(login_required, name='dispatch')
class NewRecipe(CreateView):
    """
    Создаем новый рецепт.
    """
    form_class = RecipeForm
    template_name = "recipes/form_recipe.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super(NewRecipe, self).form_valid(form)
        return response

    def form_valid(self, form):
        self.object = form.save(commit=False)
        for ingredient in form.cleaned_data['ingredients']:
            recipe_ingredient = RecipeIngredient()
            recipe_ingredient.ingredient = self.object
            recipe_ingredient.recipe = ingredient
            recipe_ingredient.save()
        return super(ModelFormMixin, self).form_valid(form)


# def get_ingredients(request):
#     """
#     Parse POST request body for ingredient names and their respective amounts.
#     """
#     ingredients = {}
#     for key, name in request.POST.items():
#         if key.startswith('nameIngredient'):
#             num = key.split('_')[1]
#             ingredients[name] = request.POST[
#                 f'valueIngredient_{num}'
#             ]
#
#     return ingredients
#
#
# def save_recipe(request, form):
#     """
#     Create and save a Recipe instance with neccessary m2m relationships.
#     """
#     try:
#         with transaction.atomic():
#             recipe = form.save(commit=False)
#             recipe.author = request.user
#             recipe.save()
#
#             objs = []
#             ingredients = get_ingredients(request)
#             for name, quantity in ingredients.items():
#                 ingredient = get_object_or_404(Ingredient, title=name)
#                 objs.append(
#                     RecipeIngredient(
#                         recipe=recipe,
#                         ingredient=ingredient,
#                         quantity=Decimal(quantity.replace(',', '.'))
#                     )
#                 )
#             RecipeIngredient.objects.bulk_create(objs)
#
#             form.save_m2m()
#             return recipe
#     except IntegrityError:
#         raise HttpResponseBadRequest
#
#
# def recipe_new(request):
#     form = RecipeForm(request.POST or None, files=request.FILES or None)
#     if form.is_valid():
#         recipe = save_recipe(request, form)
#
#         return redirect(
#             'slug_recipe_view', recipe_id=recipe.id, slug=recipe.slug
#         )

# return render(request, 'recipes/formRecipe.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class EditRecipe(UpdateView):
    """
    Изменяем содержимое рецепта.
    """
    model = Recipe  # Ingredient
    template_name = 'recipes/form_recipe.html'
    fields = ['title', 'tags', 'ingredients',
              'cooking_time', 'text', 'image', ]

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Проверяем, что только автор рецепта может его изменить.
        """
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect(reverse('slug_recipe_view', kwargs={
                'slug': obj.slug,
                'recipe_id': obj.id}))
        response = super(EditRecipe, self).dispatch(request, *args, **kwargs)
        return response

    # def get_context_data(self, **kwargs):
    #     """
    #     Изменяем шаблон в зависимости сценария.
    #     """
    #     context = super().get_context_data(**kwargs)
    #     context['source'] = True
    #     return context


@method_decorator(login_required, name='dispatch')
class DeleteRecipe(DeleteView):
    """
    Удаляем рецепт.
    """
    model = Recipe
    template_name = 'recipes/form_recipe.html'
    success_url = reverse_lazy('index')


def profile_view(request, username):
    """
    TBD
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


@login_required
def purchases_download(request):
    """
    TBD
    """
    ingredients = request.user.purchases.select_related('recipe').order_by(
        'recipe__ingredients__title').values(
        'recipe__ingredients__title', 'recipe__ingredients__unit_measure'
    ).annotate(amount=Sum('recipe__ingredients_amounts__quantity')).all()

    pdf = generate_pdf('recipes/includes/shop_list.html',
                       {'ingredients': ingredients})

    return FileResponse(io.BytesIO(pdf), filename='ingredients.pdf',
                        as_attachment=True)


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
