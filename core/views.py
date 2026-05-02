from django.db import connection, OperationalError
from django.http import JsonResponse
from django.views.generic import TemplateView


class ContactView(TemplateView):
    """Renders the static contact page template."""

    template_name = "contact.html"


class ImpressumView(TemplateView):
    """Legal notice page (Impressum) as required by German law (TMG §5)."""

    template_name = "impressum.html"


class PrivacyView(TemplateView):
    """Privacy policy page (GDPR)."""

    template_name = "privacy.html"


def health_check(request):
    """Return 200 if the app and database are reachable, 503 otherwise."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok"})
    except OperationalError as e:
        return JsonResponse({"status": "error", "detail": str(e)}, status=503)
