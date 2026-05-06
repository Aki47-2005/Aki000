from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="dashboard", permanent=False)),
    path("accounts/", include("apps.accounts.urls")),
    path("students/", include("apps.students.urls")),
    path("courses/", include("apps.courses.urls")),
    path("payments/", include("apps.payments.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("reports/", include("apps.reports.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
