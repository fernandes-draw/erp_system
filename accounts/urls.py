from django.urls import path
from .views import SignUpView, DashboardView, ProfileUpdateView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]
