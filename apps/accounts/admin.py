from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AuditLog, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role", "created_at")}),)
    readonly_fields = ("created_at",)
    list_display = ("username", "email", "role", "is_staff", "created_at")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "ip_address", "timestamp")
    search_fields = ("user__username", "action", "ip_address")
    list_filter = ("timestamp",)
