from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from common.mixins import CacheMixin
from django.contrib.auth import login

from .forms import CustomUserCreationForm
from .models import User

class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


# class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
#     template_name = "profile.html"
#     # form_class = ProfileForm
#     success_url = reverse_lazy("profile")
