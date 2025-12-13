import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.db import OperationalError, transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView

from contact.forms import ContactRequestForm
from contact.models import ContactRequest

logger = logging.getLogger(__name__)


class ContactRequestView(SuccessMessageMixin, CreateView):
    """
    Handles public contact form submissions:
    - Saves a ContactRequest
    - Sends a notification email after successful DB commit
    """

    form_class = ContactRequestForm
    model = ContactRequest
    template_name = "contact.html"
    success_message = "Thank you. Your message was sent."
    success_url = reverse_lazy("doridoro:index")

    def form_valid(self, form: ContactRequestForm):
        """
        Save the object inside an atomic transaction,
        and send the email *after* the DB commit succeeds.
        """
        try:
            with transaction.atomic():
                self.object = form.save()

                # Ensure email is only sent if DB commit succeeds
                transaction.on_commit(lambda: form.send_email())
        except OperationalError as e:
            # DB-level problems (migrations missing, DB down, etc.)
            logger.exception("Database error while handling contact form.")
            form.add_error(
                None,
                f"We are experiencing a database issue: '{e}'. "
                "Please try again later.",
            )
            return self.form_invalid(form)

        except Exception as e:
            # Any unexpected error (email, logic error, etc.)
            logger.exception("Unexpected error while handling contact form.")
            form.add_error(
                None,
                f"An unexpected error occurred while sending your message: '{e}'. "
                "Please try again later.",
            )
            return self.form_invalid(form)

        return super().form_valid(form)
