from django.contrib import admin

from .models import Course, Registration


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "department", "semester", "capacity", "day_of_week", "start_time", "end_time")
    search_fields = ("code", "title", "department")
    list_filter = ("department", "semester")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "semester", "status", "registered_at")
    list_filter = ("semester", "status")
    search_fields = ("student__reg_number", "course__code")
