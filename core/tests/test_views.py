from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate


class HealthCheckTestCase(TestCase):
    def test_returns_200(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)

    def test_returns_json_ok(self):
        import json
        response = self.client.get(reverse("health"))
        data = json.loads(response.content)
        self.assertEqual(data["status"], "ok")

    def test_content_type_is_json(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response["Content-Type"], "application/json")


class StaticPagesTestCase(TestCase):
    def setUp(self):
        activate("en")

    def test_impressum_returns_200(self):
        response = self.client.get(reverse("impressum"))
        self.assertEqual(response.status_code, 200)

    def test_impressum_uses_correct_template(self):
        response = self.client.get(reverse("impressum"))
        self.assertTemplateUsed(response, "impressum.html")

    def test_privacy_returns_200(self):
        response = self.client.get(reverse("privacy"))
        self.assertEqual(response.status_code, 200)

    def test_privacy_uses_correct_template(self):
        response = self.client.get(reverse("privacy"))
        self.assertTemplateUsed(response, "privacy.html")
