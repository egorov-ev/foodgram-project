from django.urls import include, path

from . import views

recipes_urls = [
    path('new/', views.NewRecipe.as_view(), name='new_recipe'),
    path('<int:recipe_id>/<slug:slug>/edit/', views.EditRecipe.as_view(),
         name='edit_recipe'),
    path('<int:recipe_id>/<slug:slug>/delete/', views.DeleteRecipe.as_view(),
         name='delete_recipe'),
    path('<int:recipe_id>/', views.recipe_view, name='view_recipe', ),
    path('<int:recipe_id>/<slug:slug>/', views.slug_recipe_view,
         name='slug_recipe_view', ),
]

purchases_urls = [
    path('', views.purchases, name='purchases'),
    path('download/', views.purchases_download, name='purchases_download'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchases/', views.purchases, name='purchases'),
    path('<str:username>/', views.profile_view, name='profile_view'),
    path('recipes/', include(recipes_urls)),
    path('purchases/', include(purchases_urls)),
]
