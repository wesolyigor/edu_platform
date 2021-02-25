
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm


class SignupPageView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'