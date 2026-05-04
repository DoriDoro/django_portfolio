from django.test import TestCase

from doridoro.models import Achievement


class ActiveManagerTestCase(TestCase):
    """Tests ActiveManager behaviour using Achievement as a concrete model."""

    @classmethod
    def setUpTestData(cls):
        Achievement(title_en="Active One", content_en="yes", active=True).save(clean=False)
        Achievement(title_en="Active Two", content_en="yes", active=True).save(clean=False)
        Achievement(title_en="Inactive One", content_en="yes", active=False).save(clean=False)

    def test_returns_only_active_records(self):
        qs = Achievement.active_achievements.all()
        for obj in qs:
            self.assertTrue(obj.active)

    def test_excludes_inactive_records(self):
        titles = list(Achievement.active_achievements.values_list("title_en", flat=True))
        self.assertNotIn("Inactive One", titles)

    def test_count_matches_active_only(self):
        total = Achievement.objects.count()
        active = Achievement.active_achievements.count()
        self.assertEqual(active, total - 1)
