from django.urls import path

from . import views

urlpatterns = [
    path("author/", views.about_author, name="author"),
    path("tech/", views.about_tech, name="tech"),
]
