from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.students.models import Student


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    transaction_ref = models.CharField(max_length=100, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.student.reg_number} - {self.transaction_ref}"


class Clearance(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="clearance")
    is_cleared = models.BooleanField(default=False)
    cleared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    cleared_at = models.DateTimeField(null=True, blank=True)

    def approve(self, user):
        self.is_cleared = True
        self.cleared_by = user
        self.cleared_at = timezone.now()
        self.save(update_fields=["is_cleared", "cleared_by", "cleared_at"])

    def reject(self, user):
        self.is_cleared = False
        self.cleared_by = user
        self.cleared_at = timezone.now()
        self.save(update_fields=["is_cleared", "cleared_by", "cleared_at"])

    def __str__(self):
        return f"{self.student.reg_number} cleared={self.is_cleared}"
