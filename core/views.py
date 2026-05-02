from django.views.generic import TemplateView


class ContactView(TemplateView):
    """Renders the static contact page template."""

    template_name = "contact.html"
