import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView

from contact.forms import ContactRequestForm
from contact.models import ContactRequest

logger = logging.getLogger(__name__)


class ContactRequestView(SuccessMessageMixin, CreateView):
    """Handles public contact form submissions; saves a ContactRequest and sends an email after commit."""

    form_class = ContactRequestForm
    model = ContactRequest
    template_name = "contact.html"
    success_message = "Thank you. Your message was sent."
    success_url = reverse_lazy("doridoro:index")

    def form_valid(self, form: ContactRequestForm):
        """Save inside an atomic transaction; email is dispatched via on_commit after the DB write succeeds."""
        try:
            with transaction.atomic():
                self.object = form.save()

                # Ensure email is only sent if DB commit succeeds
                transaction.on_commit(lambda: form.send_email())
        except Exception:
            logger.exception("Unexpected error while handling contact form.")
            form.add_error(
                None, "An unexpected error occurred. Please try again later."
            )
            return self.form_invalid(form)

        return super().form_valid(form)
