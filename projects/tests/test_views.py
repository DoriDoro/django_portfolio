import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate

from projects.models import Project, Skill


class ProjectViewsBase(TestCase):
    BASE = {
        "tag": Project.TagChoices.PERSONAL,
        "legend": "A legend",
        "create_date": datetime.date(2023, 1, 1),
        "skill_set_en": "<p>Python</p>",
        "introduction_en": "<p>Intro</p>",
        "experience_en": "<p>Experience</p>",
    }

    @classmethod
    def setUpTestData(cls):
        cls.active_project = Project(**{**cls.BASE, "name": "Active Project"})
        cls.active_project.save(clean=False)

        cls.inactive_project = Project(
            **{**cls.BASE, "name": "Inactive Project", "active": False}
        )
        cls.inactive_project.save(clean=False)

    def setUp(self):
        activate("en")


class PortfolioListViewTestCase(ProjectViewsBase):
    def test_get_returns_200(self):
        response = self.client.get(reverse("projects:portfolio"))
        self.assertEqual(response.status_code, 200)

    def test_uses_portfolio_template(self):
        response = self.client.get(reverse("projects:portfolio"))
        self.assertTemplateUsed(response, "portfolio.html")

    def test_only_active_projects_shown(self):
        response = self.client.get(reverse("projects:portfolio"))
        names = [p.name for p in response.context["projects"]]
        self.assertIn("Active Project", names)
        self.assertNotIn("Inactive Project", names)

    def test_context_has_filter_tags(self):
        response = self.client.get(reverse("projects:portfolio"))
        self.assertIn("filter_tags", response.context)


class PortfolioDetailViewTestCase(ProjectViewsBase):
    def test_get_active_project_returns_200(self):
        url = reverse("projects:portfolio-detail", kwargs={"slug": self.active_project.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_uses_detail_template(self):
        url = reverse("projects:portfolio-detail", kwargs={"slug": self.active_project.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "portfolio_details.html")

    def test_context_has_project(self):
        url = reverse("projects:portfolio-detail", kwargs={"slug": self.active_project.slug})
        response = self.client.get(url)
        self.assertEqual(response.context["project"].name, "Active Project")

    def test_inactive_project_returns_404(self):
        url = reverse(
            "projects:portfolio-detail", kwargs={"slug": self.inactive_project.slug}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_unknown_slug_returns_404(self):
        url = reverse("projects:portfolio-detail", kwargs={"slug": "does-not-exist"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_skills_prefetched(self):
        skill = Skill(
            name_en="Python",
            category=Skill.CategoryChoices.PROGRAMMING_SKILLS,
            sub_category=Skill.SubCategory.BACKEND,
        )
        skill.save(clean=False)
        self.active_project.skills.add(skill)

        url = reverse("projects:portfolio-detail", kwargs={"slug": self.active_project.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(skill, self.active_project.skills.all())
