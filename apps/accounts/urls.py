from django.urls import path

from .views import SecureLoginView, dashboard, logout_view

urlpatterns = [
    path("login/", SecureLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
]
