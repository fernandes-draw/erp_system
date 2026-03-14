from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.views.generic import TemplateView


class SignUpView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
    # Função que define QUEM  pode acessar essa página
    def test_func(self):
        
        # Apenas usuários logados que sejam 'staff' (gerentes/admin)
        return self.request.user.is_staff


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"
