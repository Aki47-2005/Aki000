from django.conf import settings
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    full_name = models.CharField(max_length=150)
    reg_number = models.CharField(max_length=50, unique=True)
    programme = models.CharField(max_length=150)
    year_of_study = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.reg_number})"
