from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from apps.notifications.models import Notification
from apps.students.models import Student

from .forms import PaymentForm
from .models import Clearance, Payment


def admin_required(user):
    return user.is_authenticated and user.is_admin_role


@login_required
def submit_payment(request):
    student = get_object_or_404(Student, user=request.user)
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        payment = form.save(commit=False)
        payment.student = student
        payment.save()
        Notification.objects.create(student=student, message="Payment submitted for verification.", type=Notification.Types.PAYMENT)
        messages.success(request, "Payment submitted.")
        return redirect("dashboard")
    return render(request, "payments/form.html", {"form": form})


@user_passes_test(admin_required)
def payment_queue(request):
    payments = Payment.objects.select_related("student").order_by("-updated_at")
    status = request.GET.get("status", "").strip()
    if status:
        payments = payments.filter(status=status)
    return render(request, "payments/queue.html", {"payments": payments, "status": status, "statuses": Payment.Status})


@user_passes_test(admin_required)
def decide_payment(request, pk, decision):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        payment.status = Payment.Status.VERIFIED if decision == "verify" else Payment.Status.REJECTED
        payment.save(update_fields=["status", "updated_at"])
        Notification.objects.create(
            student=payment.student,
            message=f"Payment {payment.transaction_ref} {payment.status.lower()}.",
            type=Notification.Types.PAYMENT,
        )
        messages.success(request, "Payment decision saved.")
    return redirect("payment_queue")


@user_passes_test(admin_required)
def clearance_queue(request):
    clearances = list(Clearance.objects.select_related("student", "cleared_by").order_by("student__reg_number"))
    for clearance in clearances:
        clearance.latest_payment = clearance.student.payments.order_by("-updated_at").first()
    return render(request, "clearance.html", {"clearances": clearances})


@user_passes_test(admin_required)
def decide_clearance(request, pk, decision):
    clearance = get_object_or_404(Clearance, pk=pk)
    if request.method == "POST":
        if decision == "approve":
            clearance.approve(request.user)
            msg = "Financial clearance approved."
            note_type = Notification.Types.APPROVAL
        else:
            clearance.reject(request.user)
            msg = "Financial clearance rejected."
            note_type = Notification.Types.REJECTION
        Notification.objects.create(student=clearance.student, message=msg, type=note_type)
        messages.success(request, msg)
    return redirect("clearance_queue")
