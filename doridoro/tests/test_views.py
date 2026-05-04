import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from accounts.models import Profile
from doridoro.models import Achievement, Job, Language, SocialMedia

UserModel = get_user_model()


class DoridoroViewsBase(TestCase):
    """Creates the User(username='Doro') and Profile that every doridoro view requires."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            username="Doro", email="doro@example.com", password="TestPass0!"
        )
        cls.profile = Profile(
            user=cls.user,
            phone_number_en="+49 30 123456",
            address_en="Berlin",
            profession_en="Developer",
            motto_en="Keep going",
            introduction_en="<p>Hello</p>",
            more_details_en="<p>Details</p>",
        )
        cls.profile.save(clean=False)

    def setUp(self):
        activate("en")


class IndexViewTestCase(DoridoroViewsBase):
    def test_get_returns_200(self):
        response = self.client.get(reverse("doridoro:index"))
        self.assertEqual(response.status_code, 200)

    def test_uses_index_template(self):
        response = self.client.get(reverse("doridoro:index"))
        self.assertTemplateUsed(response, "index.html")

    def test_context_has_doridoro(self):
        response = self.client.get(reverse("doridoro:index"))
        self.assertIn("doridoro", response.context)

    def test_context_has_social_media(self):
        SocialMedia(name="LinkedIn", url="https://linkedin.com/test").save(clean=False)
        response = self.client.get(reverse("doridoro:index"))
        self.assertIn("social_media", response.context)


class AboutViewTestCase(DoridoroViewsBase):
    def test_get_returns_200(self):
        response = self.client.get(reverse("doridoro:about"))
        self.assertEqual(response.status_code, 200)

    def test_uses_about_template(self):
        response = self.client.get(reverse("doridoro:about"))
        self.assertTemplateUsed(response, "about.html")

    def test_context_keys(self):
        response = self.client.get(reverse("doridoro:about"))
        for key in (
            "doridoro",
            "current_positions",
            "projects_count",
            "skills_count",
            "achievements",
        ):
            self.assertIn(key, response.context)

    def test_achievements_in_context(self):
        Achievement(title_en="My Goal", content_en="Done").save(clean=False)
        response = self.client.get(reverse("doridoro:about"))
        titles = [a[0] for a in response.context["achievements"]]
        self.assertIn("My Goal", titles)


class SkillsViewTestCase(DoridoroViewsBase):
    def test_get_returns_200(self):
        response = self.client.get(reverse("doridoro:skills"))
        self.assertEqual(response.status_code, 200)

    def test_context_has_skill_groups(self):
        response = self.client.get(reverse("doridoro:skills"))
        for key in ("programming_skills", "soft_skills", "strength", "languages"):
            self.assertIn(key, response.context)

    def test_languages_in_context(self):
        Language(name_en="German", level=Language.LevelChoices.NATIVE).save(clean=False)
        response = self.client.get(reverse("doridoro:skills"))
        self.assertIn("German", str(response.context["languages"]))


class ResumeViewTestCase(DoridoroViewsBase):
    JOB_BASE = {
        "position_en": "Engineer",
        "company_name": "Acme",
        "job_type": Job.JobTypeChoices.EMPLOYED,
        "work_type": Job.WorkTypeChoices.REMOTE,
        "start_date": datetime.date(2021, 1, 1),
        "end_date": datetime.date(2022, 1, 1),
        "until_present": False,
    }

    def test_get_returns_200(self):
        response = self.client.get(reverse("doridoro:resume"))
        self.assertEqual(response.status_code, 200)

    def test_context_has_job_groups(self):
        response = self.client.get(reverse("doridoro:resume"))
        for key in ("jobs_formation", "jobs_mentoring", "jobs_experience"):
            self.assertIn(key, response.context)

    def test_employed_job_goes_to_experience(self):
        Job(**self.JOB_BASE).save(clean=False)
        response = self.client.get(reverse("doridoro:resume"))
        positions = [j.position_en for j in response.context["jobs_experience"]]
        self.assertIn("Engineer", positions)

    def test_formation_job_goes_to_formation(self):
        Job(
            **{
                **self.JOB_BASE,
                "position_en": "Bootcamp",
                "job_type": Job.JobTypeChoices.FORMATION,
                "company_name": "School",
            }
        ).save(clean=False)
        response = self.client.get(reverse("doridoro:resume"))
        positions = [j.position_en for j in response.context["jobs_formation"]]
        self.assertIn("Bootcamp", positions)
