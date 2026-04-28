import logging

from django.conf import settings
from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.html import strip_tags
from textwrap import dedent

from contact.models import ContactRequest

logger = logging.getLogger(__name__)


class ContactRequestForm(forms.ModelForm):
    """
    Public contact form used on the website to create ContactRequest objects
    and notify the team by email.
    """

    class Meta:
        model = ContactRequest
        exclude = ["submitted_at", "category"]
        labels = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "subject": "",
            "message": "",
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your first name",
                    "aria-label": "Your first name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your last name",
                    "aria-label": "Your last name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your email address",
                    "aria-label": "Your email address",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "What is your request about?",
                    "aria-label": "What is your request about?",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your message",
                    "aria-label": "Your message",
                    "rows": 6,
                }
            ),
        }

    # --- Normalization / extra validation ---

    def clean_first_name(self):
        first_name = (self.cleaned_data.get("first_name") or "").strip()
        if not first_name:
            raise ValidationError("Please provide a first name.")
        return first_name

    def clean_last_name(self):
        last_name = (self.cleaned_data.get("last_name") or "").strip()
        return last_name

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise ValidationError("Please provide an email address.")
        return email

    def clean_subject(self):
        subject = (self.cleaned_data.get("subject") or "").strip()
        if not subject:
            raise ValidationError("Please provide a subject.")
        return subject

    def clean_message(self):
        message = (self.cleaned_data.get("message") or "").strip()
        # Enforce a minimum length / anti-spam check
        if len(strip_tags(message)) < 10:
            raise forms.ValidationError("Please provide a more detailed message.")
        return message

    # --- Email sending ---
    def send_email(self):
        """
        Sends an email notification based on the validated form data.

        Assumes `is_valid()` has already been called.
        """
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data.get("last_name") or ""
        name = f"{first_name} {last_name}".strip()
        email = self.cleaned_data["email"]
        subject = self.cleaned_data["subject"]
        message_html = self.cleaned_data["message"]

        # Plain-text version: strip HTML tags from the message body
        message_plain = strip_tags(message_html)

        # Email subject for your team
        email_subject = (
            f"[{getattr(settings, 'PROJECT_NAME', '').strip() or 'Website'}] "
            "Contact form submission"
        )

        body_plain = dedent(f"""\
            New contact form submission:

            Name:  {name}
            Email: {email}
            Subject: {subject}

            ------------------------------
            Message:
            {message_plain}
        """).strip()

        recipient = getattr(settings, "CONTACT_EMAIL", "").strip()
        if not recipient:
            raise RuntimeError("CONTACT_EMAIL setting is missing or empty.")

        try:
            send_mail(
                subject=email_subject,
                message=body_plain,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception:
            logger.exception(f"Failed contact form submission for: '{email}'.")
