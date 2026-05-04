from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import activate


VALID_POST = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada@example.com",
    "subject": "Hello",
    "message": "<p>This is a long enough message to pass validation.</p>",
}


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_EMAIL="owner@portfolio.com",
    DEFAULT_FROM_EMAIL="noreply@portfolio.com",
    PROJECT_NAME="TestPortfolio",
)
class ContactRequestViewTestCase(TestCase):
    def setUp(self):
        activate("en")
        self.url = reverse("contact:contact_me")

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact.html")

    def test_post_valid_form_redirects(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(self.url, data=VALID_POST)
        self.assertEqual(response.status_code, 302)

    def test_post_valid_form_sends_email(self):
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(self.url, data=VALID_POST)
        self.assertEqual(len(mail.outbox), 1)

    def test_post_invalid_form_returns_200_with_errors(self):
        response = self.client.post(self.url, data={**VALID_POST, "first_name": "   "})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "first_name", "This field is required.")
