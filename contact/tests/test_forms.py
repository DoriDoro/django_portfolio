from django.core import mail
from django.test import TestCase, override_settings

from contact.forms import ContactRequestForm


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
class ContactRequestFormTestCase(TestCase):
    def _get_form(self, data=None):
        return ContactRequestForm(data=data or VALID_POST)

    def test_valid_form_all_fields(self):
        form = self._get_form()
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_form_no_last_name(self):
        data = {**VALID_POST, "last_name": ""}
        self.assertTrue(self._get_form(data).is_valid())

    def test_invalid_blank_first_name(self):
        form = self._get_form({**VALID_POST, "first_name": "   "})
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_invalid_blank_email(self):
        form = self._get_form({**VALID_POST, "email": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_invalid_blank_subject(self):
        form = self._get_form({**VALID_POST, "subject": "   "})
        self.assertFalse(form.is_valid())
        self.assertIn("subject", form.errors)

    def test_invalid_message_too_short(self):
        form = self._get_form({**VALID_POST, "message": "<p>Hi</p>"})
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_send_email_puts_message_in_outbox(self):
        form = self._get_form()
        self.assertTrue(form.is_valid())
        form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("ada@example.com", mail.outbox[0].body)

    def test_send_email_missing_contact_email_raises(self):
        with override_settings(CONTACT_EMAIL=""):
            form = ContactRequestForm(data=VALID_POST)
            form.is_valid()
            with self.assertRaises(RuntimeError):
                form.send_email()
