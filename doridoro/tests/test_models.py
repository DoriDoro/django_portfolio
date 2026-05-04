import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from doridoro.models import Achievement, Degree, Job, Language, SocialMedia


class AchievementTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.achievement = Achievement(title_en="Run a marathon", content_en="I did it!")
        cls.achievement.save(clean=False)

    def test_str(self):
        self.assertIn("Run a marathon", str(self.achievement))

    def test_normalize_strips_whitespace(self):
        a = Achievement(title_en="  Swim  ", content_en="Done")
        a.save(clean=False)
        self.assertEqual(a.title_en, "Swim")

    def test_duplicate_title_case_insensitive_raises(self):
        dup = Achievement(title_en="run a marathon", content_en="Again")
        with self.assertRaises(Exception):
            dup.save(clean=False)

    def test_active_manager_excludes_inactive(self):
        Achievement(title_en="Inactive one", content_en="x", active=False).save(clean=False)
        titles = list(Achievement.active_achievements.values_list("title_en", flat=True))
        self.assertNotIn("Inactive one", titles)
        self.assertIn("Run a marathon", titles)


class DegreeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.degree = Degree(
            organization="MIT",
            degree_en="Computer Science",
            url="https://mit.edu",
        )
        cls.degree.save(clean=False)

    def test_str(self):
        self.assertIn("MIT", str(self.degree))

    def test_normalize_strips_whitespace(self):
        d = Degree(organization="  Harvard  ", degree_en="  Physics  ")
        d.save(clean=False)
        self.assertEqual(d.organization, "Harvard")
        self.assertEqual(d.degree_en, "Physics")

    def test_duplicate_org_degree_raises(self):
        dup = Degree(organization="MIT", degree_en="Computer Science")
        with self.assertRaises(Exception):
            dup.save(clean=False)

    def test_active_manager_excludes_inactive(self):
        Degree(organization="Old School", degree_en="Art", active=False).save(clean=False)
        orgs = list(Degree.active_degrees.values_list("organization", flat=True))
        self.assertNotIn("Old School", orgs)


class JobTestCase(TestCase):
    BASE = {
        "position_en": "Backend Developer",
        "company_name": "Acme Corp",
        "job_type": Job.JobTypeChoices.EMPLOYED,
        "work_type": Job.WorkTypeChoices.REMOTE,
        "start_date": datetime.date(2022, 1, 1),
        "end_date": datetime.date(2023, 1, 1),
        "until_present": False,
    }

    @classmethod
    def setUpTestData(cls):
        cls.job = Job(**cls.BASE)
        cls.job.save(clean=False)

    def test_str(self):
        self.assertIn("EMPLOYED", str(self.job))

    def test_active_manager_excludes_inactive(self):
        Job(**{**self.BASE, "position_en": "Old Job", "active": False}).save(clean=False)
        positions = list(Job.active_jobs.values_list("position_en", flat=True))
        self.assertNotIn("Old Job", positions)

    def test_no_end_date_and_not_until_present_raises(self):
        job = Job(**{**self.BASE, "end_date": None, "until_present": False})
        with self.assertRaises(ValidationError):
            job.validate_constraints()

    def test_until_present_with_end_date_raises(self):
        job = Job(**{**self.BASE, "end_date": datetime.date(2023, 1, 1), "until_present": True})
        with self.assertRaises(ValidationError):
            job.validate_constraints()

    def test_end_date_before_start_raises(self):
        job = Job(
            **{
                **self.BASE,
                "start_date": datetime.date(2023, 1, 1),
                "end_date": datetime.date(2022, 1, 1),
            }
        )
        with self.assertRaises(ValidationError):
            job.validate_constraints()

    def test_employed_type_requires_company_name(self):
        job = Job(
            **{
                **self.BASE,
                "position_en": "No Company",
                "company_name": "",
                "job_type": Job.JobTypeChoices.EMPLOYED,
            }
        )
        with self.assertRaises(ValidationError):
            job.validate_constraints()


class LanguageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.language = Language(name_en="Python", level=Language.LevelChoices.C2)
        cls.language.save(clean=False)

    def test_str(self):
        self.assertIn("Python", str(self.language))
        self.assertIn("C2", str(self.language))

    def test_duplicate_name_raises(self):
        dup = Language(name_en="python", level=Language.LevelChoices.A1)
        with self.assertRaises(Exception):
            dup.save(clean=False)

    def test_active_manager_excludes_inactive(self):
        Language(name_en="Inactive Lang", level=Language.LevelChoices.A1, active=False).save(
            clean=False
        )
        names = list(Language.active_languages.values_list("name_en", flat=True))
        self.assertNotIn("Inactive Lang", names)


class SocialMediaTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.social = SocialMedia(name="GitHub", url="https://github.com/test")
        cls.social.save(clean=False)

    def test_str(self):
        self.assertIn("GitHub", str(self.social))

    def test_active_manager_excludes_inactive(self):
        SocialMedia(name="Hidden", url="https://hidden.com", active=False).save(clean=False)
        names = list(SocialMedia.active_social_medias.values_list("name", flat=True))
        self.assertNotIn("Hidden", names)
        self.assertIn("GitHub", names)
