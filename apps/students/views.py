from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student


def admin_required(user):
    return user.is_authenticated and user.is_admin_role


@login_required
def profile(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, "students/profile.html", {"student": student})


@user_passes_test(admin_required)
def student_list(request):
    students = Student.objects.select_related("user")
    query = request.GET.get("q", "").strip()
    programme = request.GET.get("programme", "").strip()
    year = request.GET.get("year", "").strip()
    if query:
        students = students.filter(
            Q(full_name__icontains=query) | Q(reg_number__icontains=query) | Q(user__username__icontains=query)
        )
    if programme:
        students = students.filter(programme=programme)
    if year:
        students = students.filter(year_of_study=year)
    context = {
        "students": students,
        "query": query,
        "programme": programme,
        "year": year,
        "programmes": Student.objects.order_by("programme").values_list("programme", flat=True).distinct(),
        "years": Student.objects.order_by("year_of_study").values_list("year_of_study", flat=True).distinct(),
    }
    return render(request, "students/list.html", context)


@user_passes_test(admin_required)
def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Student profile created.")
        return redirect("student_list")
    return render(request, "students/form.html", {"form": form, "title": "Create Student"})


@user_passes_test(admin_required)
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, "Student profile updated.")
        return redirect("student_list")
    return render(request, "students/form.html", {"form": form, "title": "Update Student"})


@user_passes_test(admin_required)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student profile deleted.")
        return redirect("student_list")
    return render(request, "confirm_delete.html", {"object": student})
