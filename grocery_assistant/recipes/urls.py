from django.urls import path, include

from . import views

recipes_urls = [
    path('new/', views.NewRecipe.as_view(),
         name='new_recipe'),
    path('<int:recipe_id>/<slug:slug>/edit/', views.EditRecipe.as_view(),
         name='edit_recipe'),
    path('<int:recipe_id>/<slug:slug>/delete/', views.DeleteRecipe.as_view(),
         name='delete_recipe'),
    path('<int:recipe_id>/<slug:slug>/', views.slug_recipe_view,
         name='slug_recipe_view', ),
    path('<int:recipe_id>/', views.recipe_view,
         name='recipe_view', ),
]

urlpatterns = [
    path('', views.index, name="index"),
    path('subscriptions/', views.subscriptions, name='subscriptions'),  # tmp
    path('favorites/', views.favorites, name='favorites'),  # tmp
    path('purchases/', views.purchases, name='purchases'),  # tmp
    path('<str:username>/', views.profile_view, name='profile_view'),
    path('recipes/', include(recipes_urls)),
    # path('purchases/', include(purchases_urls)),
]

#     path("new/", views.NewPost.as_view(), name="new_post"),
#     path("follow/", views.follow_index, name="follow_index"),
#     path("group/<slug:slug>/", views.group_posts, name="group_posts"),
#     path('<str:username>/', views.profile, name='profile'),
#     path('<str:username>/<int:post_id>/', views.post_view, name='post'),
#     path('<str:username>/<int:pk>/edit/', views.EditPost.as_view(),
#          name='post_edit'),
#     path("<str:username>/<int:post_id>/comment", views.add_comment,
#          name="add_comment"),
#     path("<str:username>/follow/", views.profile_follow,
#          name="profile_follow"),
#     path("<str:username>/unfollow/", views.profile_unfollow,
#          name="profile_unfollow"),
