from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import redirect, render

from apps.courses.models import Course, Registration
from apps.payments.models import Payment
from apps.students.models import Student

from .forms import LoginForm
from .models import AuditLog


class SecureLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        if not self.request.POST.get("remember"):
            self.request.session.set_expiry(0)
        AuditLog.objects.create(
            user=self.request.user,
            action="LOGIN",
            ip_address=self.request.META.get("REMOTE_ADDR"),
        )
        return response


def logout_view(request):
    if request.user.is_authenticated:
        AuditLog.objects.create(user=request.user, action="LOGOUT", ip_address=request.META.get("REMOTE_ADDR"))
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    registrations_by_semester = list(
        Registration.objects.values("semester").annotate(total=Count("id")).order_by("semester")[:6]
    )
    course_popularity = list(
        Course.objects.annotate(total=Count("registrations")).order_by("-total", "code")[:5]
    )
    context = {
        "total_students": Student.objects.count(),
        "total_payments": Payment.objects.count(),
        "total_registrations": Registration.objects.count(),
        "total_courses": Course.objects.count(),
        "verified_payments": Payment.objects.filter(status=Payment.Status.VERIFIED).count(),
        "pending_payments": Payment.objects.filter(status=Payment.Status.PENDING).count(),
        "registrations_by_semester": registrations_by_semester,
        "course_popularity": course_popularity,
        "recent_logs": AuditLog.objects.select_related("user")[:8],
    }
    if request.user.role == request.user.Roles.STUDENT:
        context["student"] = getattr(request.user, "student_profile", None)
        context["registrations"] = Registration.objects.filter(student=context["student"]).select_related("course") if context["student"] else []
    return render(request, "dashboard.html", context)
