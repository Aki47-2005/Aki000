def unread_notifications(request):
    if not request.user.is_authenticated or not hasattr(request.user, "student_profile"):
        return {"unread_notifications_count": 0}
    return {
        "unread_notifications_count": request.user.student_profile.notifications.filter(is_read=False).count()
    }
