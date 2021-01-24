from django.shortcuts import render

# Create your views here.

from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    template_name = "auth/SignUp.html"
    success_url = reverse_lazy("views_recipes")
