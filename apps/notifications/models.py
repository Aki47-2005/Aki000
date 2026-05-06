from django.db import models
from django.utils import timezone

from apps.students.models import Student


class Notification(models.Model):
    class Types(models.TextChoices):
        REGISTRATION = "REGISTRATION", "Registration"
        PAYMENT = "PAYMENT", "Payment"
        APPROVAL = "APPROVAL", "Approval"
        REJECTION = "REJECTION", "Rejection"
        SYSTEM = "SYSTEM", "System"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    type = models.CharField(max_length=30, choices=Types.choices, default=Types.SYSTEM)
    sent_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-sent_at"]

    def __str__(self):
        return f"{self.student.reg_number} - {self.type}"
