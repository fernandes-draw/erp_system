from django.urls import path
from .views import SignUpView, ProfileUpdateView, DashboardView, UserListView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("users/", UserListView.as_view(), name="user_list"),
]
