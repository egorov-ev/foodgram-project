from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'auth/SignUp.html'
    success_url = reverse_lazy('index')