from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserProfileForm
from django.views.generic import TemplateView, ListView
from .models import CustomUser


class SignUpView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("dashboard")
    template_name = "registration/signup.html"

    # Função que define QUEM  pode acessar essa página
    def test_func(self):
        # Somente Presidente, Diretor e Gerente podem cadastrar novos usuários
        return self.request.user.cargo in ["presidente", "diretor", "gerente"]


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = "registration/profile_update.html"
    success_url = reverse_lazy("dashboard")  # Redireciona para a home apó sucesso

    # Garante que usuário só possa editar o seo SEU PRÓPRIO perfil
    def get_object(self, queryset=None):
        return self.request.user


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = "accounts/user_list.html"
    context_object_name = "usuarios"

    def test_func(self):
        # Apenas os cargos de gestão podem ver a lista de funcionários
        return self.request.user.cargo in ["presidente", "diretor", "gerente"]
