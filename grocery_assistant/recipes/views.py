from django.shortcuts import render

# Create your views here.

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView

# from .forms import CommentForm, PostForm
# from .models import Follow, Group, Post

from .models import Ingredient, Recipe, RecipeIngredient, Tag

# from .. import recipes

User = get_user_model()
TAGS = ['breakfast', 'lunch', 'dinner']


# @cache_page(20, key_prefix="index_page")
def index(request):
    """"
    TODO добавить описание
    """
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()

    # recipe_list = Recipe.objects.select_related().all()
    recipe_list = Recipe.objects.filter(tags__title__in=tags).select_related(
        'author').prefetch_related('tags').distinct()
    paginator = Paginator(recipe_list, 10)
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


def subscriptions():
    pass
    return None


def favorites(request):
    pass
    return None


def purchases(request):  # tmp
    pass
    return None


def recipe(request):  # tmp
    pass
    return None


def profile_view(request):
    pass
    return None


#
# def follow_param(request, username):
#     """
#     Вспомогательная функция, возвращает параметры для подписки:
#         - существование подписки (true/false);
#         - количество подписчиков;
#         - количество подписок;
#         - автора;
#         - подписчика.
#     """
#     follow = {'follow': True,
#               'following_count': 0,
#               'follower_count': 0,
#               'follower': '',
#               'author': ''}
#     follower = request.user
#     author = get_object_or_404(User, username=username)
#     follow[
#         'follow'] = request.user.is_authenticated and Follow.objects.filter(
#         user_id=follower.id,
#         author_id=author.id).exists()
#     follow['following_count'] = author.follower.count()
#     follow['follower_count'] = author.following.count()
#     follow['follower'] = follower
#     follow['author'] = author
#
#     return follow
#
#
# def post_view(request, username, post_id):
#     """
#     Возвращает страницу профайл и запрошенный отдельный поста автора
#     """
#     follow = follow_param(request, username)
#     post = get_object_or_404(Post, author__username=username, pk=post_id)
#     form = CommentForm(instance=None)
#     comments = post.comments.all()
#     post_count = post.author.posts.count()
#     response = render(request,
#                       'posts/post.html',
#                       {
#                           "author": post.author,
#                           'comments': comments,
#                           "post": post,
#                           'form': form,
#                           'post_count': post_count,
#                           'follow': follow['follow'],
#                           'following_count': follow['following_count'],
#                           'follower_count': follow['follower_count'],
#                       }
#                       )
#     return response
#
#
# def group_posts(request, slug):
#     """"
#     Возвращает страницу с записями сообщества.
#     """
#     group = get_object_or_404(Group, slug=slug)
#     posts = group.posts.all()
#     paginator = Paginator(posts, 5)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     response = render(request, 'posts/group.html',
#                       {
#                           'group': group,
#                           'page': page,
#                           'paginator': paginator,
#                       }
#                       )
#     return response
#
#
# def profile(request, username):
#     """ Возвращает профайл пользователя и его посты """
#     follow = follow_param(request, username)
#     posts = follow['author'].posts.all()
#     paginator = Paginator(posts, 5)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     response = render(request,
#                       'posts/profile/profile.html',
#                       {
#                           'follow': follow['follow'],
#                           'following_count': follow['following_count'],
#                           'follower_count': follow['follower_count'],
#                           'author': follow['author'],
#                           'page': page,
#                           'paginator': paginator
#                       }
#                       )
#     return response
#
#
# @login_required
# def follow_index(request):
#     """
#     Возвращает список постов избранных авторов
#     """
#     post_list = Post.objects.filter(author__following__user=request.user)
#     paginator = Paginator(post_list, 5)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     response = render(request,
#                       "posts/follow.html",
#                       {
#                           'page': page,
#                           'paginator': paginator
#                       }
#                       )
#     return response
#
#
# @login_required
# def profile_follow(request, username):
#     """
#     Создаем подписку на автора.
#     """
#     follow = follow_param(request, username)
#     if not follow['follow']:
#         Follow.objects.create(user_id=follow['follower'].id,
#                               author_id=follow['author'].id)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#
# @login_required
# def profile_unfollow(request, username):
#     """
#     Удаляем подписку на автора.
#     """
#     follow = follow_param(request, username)
#     if follow['follow']:
#         kick_follower = Follow.objects.filter(user_id=follow['follower'].id,
#                                               author_id=follow['author'].id)
#         kick_follower.delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#
# @login_required
# def add_comment(request, username, post_id):
#     """
#     Добавляем комментарий к посту.
#     """
#     post = get_object_or_404(Post, pk=post_id, author__username=username)
#     form = CommentForm(request.POST or None)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.author = request.user
#         comment.save()
#     return redirect('post', username=username, post_id=post_id)
#
#
# @method_decorator(login_required, name='dispatch')
# class NewPost(CreateView):
#     """
#     Создаем пост пользователя.
#     """
#     form_class = PostForm
#     success_url = reverse_lazy("views_posts")
#     template_name = "posts/new.html"
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         response = super(NewPost, self).form_valid(form)
#         return response
#
#
# class EditPost(UpdateView):
#     """
#     Изменяем содержимое поста пользователя.
#     """
#     model = Post
#     template_name = 'posts/new.html'
#     fields = ['text', 'group', 'image']
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         """
#         Проверяем, что только автор поста может его изменить.
#         """
#         obj = self.get_object()
#         if obj.author != self.request.user:
#             return redirect(
#                 reverse('post', kwargs={
#                     'username': obj.author,
#                     'post_id': obj.id})
#             )
#         response = super(EditPost, self).dispatch(request, *args, **kwargs)
#         return response
#
#     def get_context_data(self, **kwargs):
#         """
#         Изменяем шаблон в зависимости сценария.
#         """
#         context = super().get_context_data(**kwargs)
#         context['source'] = True
#         return context
#
#

def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
