from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Notification


@login_required
def notification_list(request):
    student = request.user.student_profile
    return render(request, "notifications/list.html", {"notifications": student.notifications.all()})


@login_required
def mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, student=request.user.student_profile)
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    return redirect("notification_list")
