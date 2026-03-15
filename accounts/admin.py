from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Colunas que aparecem na lista de usuários
    list_display = [
        "username",
        "email",
        "cargo",
        "cor_identificadora",  # Adicionado para ver a cor na tabela
        "is_staff",
    ]

    # Campos que aparecem na tela de edição do usuário
    fieldsets = UserAdmin.fieldsets + (
        (
            "Informações Profissionais",
            {"fields": ("cargo", "avatar", "cor_identificadora")},
        ),
    )

    # Campos que aparecem na tela de criação (pelo admin)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informações Profissionais",
            {"fields": ("cargo", "avatar", "cor_identificadora")},
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
