from django.urls import path

from . import views

urlpatterns = [
    path('', views.views_recipes, name="views_recipes"),
]

recipes_urls = []

urlpatterns += [
    # path('', views.index, name='index'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchases/', views.purchases, name='purchases'),  # tmp
    path('recipe/', views.recipe, name='recipe'),  # tmp
    # path('purchases/', include(purchases_urls)),
    # path('recipe/', include(recipes_urls)),
    path('<str:username>/', views.profile_view, name='profile_view'),
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
