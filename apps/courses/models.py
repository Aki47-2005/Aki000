from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.students.models import Student


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    credit_units = models.PositiveSmallIntegerField()
    department = models.CharField(max_length=120)
    prerequisites = models.ManyToManyField("self", blank=True, symmetrical=False)
    semester = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField(default=80)
    day_of_week = models.PositiveSmallIntegerField(choices=[(i, d) for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], 1)])
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.title}"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    @property
    def seats_taken(self):
        return self.registrations.exclude(status=Registration.Status.REJECTED).count()

    @property
    def has_capacity(self):
        return self.seats_taken < self.capacity


class Registration(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="registrations")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="registrations")
    semester = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    registered_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("student", "course", "semester")
        ordering = ["-registered_at"]

    def __str__(self):
        return f"{self.student} - {self.course} ({self.semester})"

    def clean(self):
        clashes = Registration.objects.filter(
            student=self.student,
            semester=self.semester,
            course__day_of_week=self.course.day_of_week,
        ).exclude(pk=self.pk).exclude(status=self.Status.REJECTED)
        for registration in clashes.select_related("course"):
            other = registration.course
            if self.course.start_time < other.end_time and other.start_time < self.course.end_time:
                raise ValidationError(f"Timetable clash with {other.code}.")
        if not self.course.has_capacity and not self.pk:
            raise ValidationError("Course capacity has been reached.")
