from django.core.exceptions import ValidationError
from django.db import transaction

from apps.notifications.models import Notification
from apps.payments.models import Clearance

from .models import Registration


@transaction.atomic
def register_student_for_course(student, course, semester):
    clearance = Clearance.objects.filter(student=student, is_cleared=True).first()
    if not clearance:
        raise ValidationError("Financial clearance is required before course registration.")

    registration = Registration(student=student, course=course, semester=semester)
    registration.full_clean()
    registration.save()

    Notification.objects.create(
        student=student,
        message=f"Registration submitted for {course.code}.",
        type=Notification.Types.REGISTRATION,
    )
    return registration
