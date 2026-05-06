from django.urls import path

from .views import admin_reports

urlpatterns = [
    path("", admin_reports, name="admin_reports"),
]
