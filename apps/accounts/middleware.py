from .models import AuditLog


class AuditLogMiddleware:
    """Records meaningful authenticated page actions with request IPs."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            AuditLog.objects.create(
                user=request.user,
                action=f"{request.method} {request.path}",
                ip_address=self.get_client_ip(request),
            )
        return response

    @staticmethod
    def get_client_ip(request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
