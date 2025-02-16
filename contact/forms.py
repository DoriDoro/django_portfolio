from django.conf import settings
from django import forms
from django.core.mail import send_mail

from contact.models import ContactRequest


class ContactRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Your first name",
                "aira-label": "Your first name",
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Your last name",
                "aira-label": "Your last name",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Your Email Address",
                "aira-label": "Your Email Address",
            }
        )
        self.fields["subject"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "What is your request about?",
                "aira-label": "What is your request about?",
            }
        )
        self.fields["message"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Your message",
                "aira-label": "Your message",
            }
        )

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

    def send_email(self):
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data.get("last_name", None)
        name = first_name if last_name is None else f"{first_name} {last_name}"
        email = self.cleaned_data["email"]
        subject = self.cleaned_data["subject"]
        message = self.cleaned_data["message"]

        create_message = f"""
            Received a message form
            Name: {name}
            Email: {email}
            with Subject: {subject}
            ------------------

            {message}
            """

        try:
            send_mail(
                subject=f"Contact Form submission: {settings.PROJECT_NAME}",
                message=create_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL.strip()],
            )
        except Exception as e:
            print(
                "--- ERROR - FAILED Contact Form submission ---",
                "email of sender: ",
                email,
                "---> Error message: ",
                e,
            )
            raise
