from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Definindo as opções de cargo
    CARGO_CHOICES = (
        ("admin", "Administrador de Sistema"),
        ("presidente", "Presidente"),  # Proprietário da empresa
        ("diretor", "Diretor"),  # Coordena todos os gerentes
        ("gerente", "Gerente"),  # Gerencia as atividades de cada setor da empresa
        (
            "supervisor",
            "Supervisor",
        ),  # Coordena os grupos de cada funcionalidade do setor
        ("operador", "Operador"),  # Colaborador que executa o serviço.
    )

    # upload_to cria uma pasta 'avatars' dentro da sua pasta mídia
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    # Campo opcional para "Role/Cargo" que comentamos
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default="operador")

    def save(self, *args, **kwargs):
        # Lógica automática: Se for Diretor ou Gerente, ganha status de equipe (is_staff)
        if self.cargo in ["admin", "presidente", "diretor", "gerente"]:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def __str__(self):
        return self.username
