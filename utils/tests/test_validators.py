from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from utils.database.validators import validate_not_blank


class ValidateNotBlankTestCase(SimpleTestCase):
    def test_valid_string_passes(self):
        validate_not_blank("hello")

    def test_html_content_passes(self):
        validate_not_blank("<p>Some content</p>")

    def test_empty_string_raises(self):
        with self.assertRaises(ValidationError):
            validate_not_blank("")

    def test_whitespace_only_raises(self):
        with self.assertRaises(ValidationError):
            validate_not_blank("   ")

    def test_none_raises(self):
        with self.assertRaises(ValidationError):
            validate_not_blank(None)

    def test_newline_only_raises(self):
        with self.assertRaises(ValidationError):
            validate_not_blank("\n\t  ")
