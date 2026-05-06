from django.urls import path

from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("create/", views.course_create, name="course_create"),
    path("register/", views.register_course, name="register_course"),
    path("slip/", views.registration_slip, name="registration_slip"),
]
