from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from apps.students.models import Student

from .forms import CourseForm, RegistrationForm
from .models import Course, Registration
from .services import register_student_for_course
from .slips import build_registration_slip


def admin_required(user):
    return user.is_authenticated and user.is_admin_role


@user_passes_test(admin_required)
def course_list(request):
    courses = Course.objects.all()
    query = request.GET.get("q", "").strip()
    semester = request.GET.get("semester", "").strip()
    if query:
        courses = courses.filter(code__icontains=query) | courses.filter(title__icontains=query)
    if semester:
        courses = courses.filter(semester=semester)
    return render(
        request,
        "courses/list.html",
        {
            "courses": courses.distinct(),
            "query": query,
            "semester": semester,
            "semesters": Course.objects.order_by("semester").values_list("semester", flat=True).distinct(),
        },
    )


@user_passes_test(admin_required)
def course_create(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Course saved.")
        return redirect("course_list")
    return render(request, "courses/form.html", {"form": form, "title": "Create Course"})


@login_required
def register_course(request):
    student = get_object_or_404(Student, user=request.user)
    semester = request.GET.get("semester") or request.POST.get("semester") or "Semester 1"
    form = RegistrationForm(request.POST or None, semester=semester)
    if form.is_valid():
        try:
            register_student_for_course(student, form.cleaned_data["course"], form.cleaned_data["semester"])
            messages.success(request, "Course registration submitted.")
            return redirect("dashboard")
        except ValidationError as exc:
            form.add_error(None, exc)
    registrations = Registration.objects.filter(student=student, semester=semester).select_related("course")
    return render(request, "register_course.html", {"form": form, "registrations": registrations, "semester": semester})


@login_required
def registration_slip(request):
    student = get_object_or_404(Student, user=request.user)
    semester = request.GET.get("semester", "Semester 1")
    return build_registration_slip(student, semester, request)
