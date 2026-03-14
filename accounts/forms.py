from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(AdminUserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User

        # Os campos que o usuário comum pode editar
        fields = ["first_name", "last_name", "email", "avatar"]
        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "avatar": "Foto de Perfil",
        }
        help_texts = {
            "avatar": "Formatos aceitos: JPG, PNG, Máx 2MB.",
        }
