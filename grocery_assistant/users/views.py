from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm

# Create your views here.



class SignUp(CreateView):
    form_class = CreationForm
    template_name = "auth/SignUp.html"
    success_url = reverse_lazy("views_recipes")
