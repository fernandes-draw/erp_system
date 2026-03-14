from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # upload_to cria uma pasta 'avatars' dentro da sua pasta mídia
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    # Campo opcional para "Role/Cargo" que comentamos
    cargo = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username
