from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from contact.models import Category, ContactRequest


class CategoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category(name="General")
        cls.category.save(clean=False)

    def test_str(self):
        self.assertEqual(str(self.category), "General")

    def test_normalize_strips_whitespace(self):
        cat = Category(name="  Trimmed  ")
        cat.save(clean=False)
        self.assertEqual(cat.name, "Trimmed")

    def test_duplicate_name_case_insensitive_raises(self):
        duplicate = Category(name="general")
        with self.assertRaises(Exception):
            duplicate.save(clean=False)

    def test_inactive_category(self):
        cat = Category(name="Inactive", active=False)
        cat.save(clean=False)
        self.assertFalse(cat.active)

    def test_active_manager_excludes_inactive(self):
        Category(name="ActiveCat", active=True).save(clean=False)
        Category(name="InactiveCat", active=False).save(clean=False)
        names = list(Category.active_categories.values_list("name", flat=True))
        self.assertIn("ActiveCat", names)
        self.assertNotIn("InactiveCat", names)


class ContactRequestTestCase(TestCase):
    VALID_DATA = {
        "first_name": "Ada",
        "email": "ada@example.com",
        "subject": "Hello",
        "message": "<p>This is a valid message</p>",
    }

    @classmethod
    def setUpTestData(cls):
        cls.category = Category(name="Test Category")
        cls.category.save(clean=False)

    def _make_request(self, **kwargs):
        data = {**self.VALID_DATA, **kwargs}
        req = ContactRequest(**data)
        req.save(clean=False)
        return req

    def test_str(self):
        req = self._make_request()
        self.assertIn("Ada", str(req))
        self.assertIn("ada@example.com", str(req))

    def test_email_normalized_to_lowercase(self):
        req = self._make_request(email="ADA@Example.COM")
        self.assertEqual(req.email, "ada@example.com")

    def test_first_name_stripped(self):
        req = self._make_request(first_name="  Ada  ")
        self.assertEqual(req.first_name, "Ada")

    def test_duplicate_within_14_days_raises(self):
        self._make_request()
        duplicate = ContactRequest(**self.VALID_DATA)
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_duplicate_allowed_after_14_days(self):
        req = self._make_request()
        req.submitted_at = timezone.now() - timedelta(days=15)
        req.save(update_fields=["submitted_at"])

        later = ContactRequest(**self.VALID_DATA)
        later.full_clean()

    def test_inactive_category_raises(self):
        inactive = Category(name="Inactive", active=False)
        inactive.save(clean=False)
        req = ContactRequest(**self.VALID_DATA, category=inactive)
        with self.assertRaises(ValidationError):
            req.full_clean()

    def test_active_category_accepted(self):
        req = ContactRequest(**self.VALID_DATA, category=self.category)
        req.full_clean()

    def test_save_clean_false_skips_duplicate_check(self):
        self._make_request()
        second = ContactRequest(**self.VALID_DATA)
        second.save(clean=False)
