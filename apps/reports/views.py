import csv

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render

from apps.courses.models import Course, Registration
from apps.payments.models import Payment
from apps.students.models import Student


def admin_required(user):
    return user.is_authenticated and user.is_admin_role


@user_passes_test(admin_required)
def admin_reports(request):
    semester = request.GET.get("semester", "")
    programme = request.GET.get("programme", "")
    course_id = request.GET.get("course", "")
    registrations = Registration.objects.select_related("student", "course")
    if semester:
        registrations = registrations.filter(semester=semester)
    if programme:
        registrations = registrations.filter(student__programme=programme)
    if course_id:
        registrations = registrations.filter(course_id=course_id)

    if request.GET.get("format") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="registration-report.csv"'
        writer = csv.writer(response)
        writer.writerow(["Student", "Reg Number", "Programme", "Course", "Semester", "Status", "Registered At"])
        for registration in registrations:
            writer.writerow([
                registration.student.full_name,
                registration.student.reg_number,
                registration.student.programme,
                registration.course.code,
                registration.semester,
                registration.status,
                registration.registered_at,
            ])
        return response

    context = {
        "semester": semester,
        "programme": programme,
        "course_id": course_id,
        "total_students": Student.objects.count(),
        "payment_total": Payment.objects.filter(status=Payment.Status.VERIFIED).aggregate(total=Sum("amount"))["total"] or 0,
        "registrations": registrations,
        "per_course": Course.objects.annotate(total_registrations=Count("registrations")).order_by("code"),
        "courses": Course.objects.order_by("code"),
        "semesters": Course.objects.order_by("semester").values_list("semester", flat=True).distinct(),
        "programmes": Student.objects.order_by("programme").values_list("programme", flat=True).distinct(),
    }
    return render(request, "admin_reports.html", context)
