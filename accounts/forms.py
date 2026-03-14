from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Adiciona os campos que o Diretor/Gerente vai preencher ao criar o funcionário
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "cargo",
            "username",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


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
