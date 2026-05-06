from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.profile, name="student_profile"),
    path("", views.student_list, name="student_list"),
    path("create/", views.student_create, name="student_create"),
    path("<int:pk>/edit/", views.student_update, name="student_update"),
    path("<int:pk>/delete/", views.student_delete, name="student_delete"),
]
