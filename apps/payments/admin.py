from django.contrib import admin

from .models import Clearance, Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("student", "amount", "status", "transaction_ref", "updated_at")
    list_filter = ("status",)
    search_fields = ("student__reg_number", "transaction_ref")


@admin.register(Clearance)
class ClearanceAdmin(admin.ModelAdmin):
    list_display = ("student", "is_cleared", "cleared_by", "cleared_at")
    list_filter = ("is_cleared",)
