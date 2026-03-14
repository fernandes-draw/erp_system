from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import DashboardView  # Importe sua view de Dashboard aqui

urlpatterns = [
    path("admin/", admin.site.urls),
    # Centraliza tudo relacionado a usuários em /accounts/
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # Login, Logout, Reset senha
    path(
        "accounts/", include("accounts.urls")
    ),  # Seus customizados: Signup, Profile, Dashboard
    path(
        "", DashboardView.as_view(), name="dashboard"
    ),  # Define a página inicial como o Dashboard
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
