from django.urls import include, path

from . import views

recipes_urls = [
    path('new/', views.NewRecipe.as_view(),
         name='new_recipe'),
    path('<int:recipe_id>/<slug:slug>/edit/', views.EditRecipe.as_view(),
         name='edit_recipe'),
    path('<int:recipe_id>/<slug:slug>/delete/', views.DeleteRecipe.as_view(),
         name='delete_recipe'),
    path('<int:recipe_id>/', views.recipe_view,
         name='recipe_view', ),
    path('<int:recipe_id>/<slug:slug>/', views.slug_recipe_view,
         name='slug_recipe_view', ),

]

urlpatterns = [
    path('', views.index, name='index'),  # главная
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    # подписки
    path('favorites/', views.favorites, name='favorites'),  # избранное
    path('purchases/', views.purchases, name='purchases'),  # покупки
    path('<str:username>/', views.profile_view, name='profile_view'),
    # профайл автора
    path('recipes/', include(recipes_urls)),
    # path('purchases/', include(purchases_urls)),
]
