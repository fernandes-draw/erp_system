from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm  # Mantemos o seu form de edição
    model = CustomUser
    
    # Colunas que aparecem na lista de usuários
    list_display = [
        "username",
        "email",
        "cargo", # Novo
        "is_staff",
        "is_active",
    ]

    # Campos que aparecem na tela de edição do usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Profissionais', {'fields': ('cargo', 'avatar')}),
    )

    # Campos que aparecem na tela de criação (pelo admin)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Profissionais', {'fields': ('cargo', 'avatar')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)