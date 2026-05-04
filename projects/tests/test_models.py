import datetime

from django.test import TestCase

from projects.models import Project, Skill


class SkillTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.skill = Skill(
            name_en="Django",
            category=Skill.CategoryChoices.PROGRAMMING_SKILLS,
            sub_category=Skill.SubCategory.BACKEND,
        )
        cls.skill.save(clean=False)

    def test_str(self):
        self.assertIn("Django", str(self.skill))
        self.assertIn("PROGRAMMING_SKILLS", str(self.skill))

    def test_normalize_strips_whitespace(self):
        skill = Skill(
            name_en="  Flask  ",
            category=Skill.CategoryChoices.PROGRAMMING_SKILLS,
            sub_category=Skill.SubCategory.BACKEND,
        )
        skill.save(clean=False)
        self.assertEqual(skill.name_en, "Flask")

    def test_duplicate_name_per_category_raises(self):
        dup = Skill(
            name_en="django",
            category=Skill.CategoryChoices.PROGRAMMING_SKILLS,
            sub_category=Skill.SubCategory.BACKEND,
        )
        with self.assertRaises(Exception):
            dup.save(clean=False)

    def test_same_name_different_category_allowed(self):
        soft = Skill(
            name_en="Django",
            category=Skill.CategoryChoices.SOFT_SKILLS,
        )
        soft.save(clean=False)

    def test_programming_skill_requires_sub_category(self):
        from django.core.exceptions import ValidationError

        skill = Skill(
            name_en="NoSub",
            category=Skill.CategoryChoices.PROGRAMMING_SKILLS,
            sub_category="",
        )
        with self.assertRaises(ValidationError):
            skill.validate_constraints()

    def test_strength_requires_content(self):
        from django.core.exceptions import ValidationError

        skill = Skill(
            name_en="Strong",
            category=Skill.CategoryChoices.STRENGTH,
            content="",
        )
        with self.assertRaises(ValidationError):
            skill.validate_constraints()

    def test_active_manager_excludes_inactive(self):
        Skill(
            name_en="Inactive Skill",
            category=Skill.CategoryChoices.SOFT_SKILLS,
            active=False,
        ).save(clean=False)
        names = list(Skill.active_skills.values_list("name_en", flat=True))
        self.assertNotIn("Inactive Skill", names)

    def test_display_active_manager_requires_display_flag(self):
        Skill(
            name_en="Hidden Skill",
            category=Skill.CategoryChoices.SOFT_SKILLS,
            display_skill=False,
            active=True,
        ).save(clean=False)
        Skill(
            name_en="Visible Skill",
            category=Skill.CategoryChoices.SOFT_SKILLS,
            display_skill=True,
            active=True,
        ).save(clean=False)
        names = list(Skill.display_active_skills.values_list("name_en", flat=True))
        self.assertIn("Visible Skill", names)
        self.assertNotIn("Hidden Skill", names)


class ProjectTestCase(TestCase):
    BASE = {
        "name": "My Portfolio",
        "tag": Project.TagChoices.PERSONAL,
        "legend": "A legend",
        "create_date": datetime.date(2023, 1, 1),
        "skill_set_en": "<p>Python</p>",
        "introduction_en": "<p>Intro</p>",
        "experience_en": "<p>Experience</p>",
    }

    @classmethod
    def setUpTestData(cls):
        cls.project = Project(**cls.BASE)
        cls.project.save(clean=False)

    def test_str(self):
        self.assertIn("My Portfolio", str(self.project))

    def test_slug_auto_generated(self):
        self.assertEqual(self.project.slug, "my-portfolio")

    def test_slug_unique_counter_on_collision(self):
        # "My Portfolio!" slugifies to the same "my-portfolio"
        # but passes the unique name constraint
        second = Project(**{**self.BASE, "name": "My Portfolio!"})
        second.save(clean=False)
        self.assertEqual(second.slug, "my-portfolio-1")

    def test_slug_regenerated_when_name_changes(self):
        project = Project(**{**self.BASE, "name": "Original Project"})
        project.save(clean=False)
        self.assertEqual(project.slug, "original-project")

        project.name = "Renamed Project"
        project.save(clean=False)
        self.assertEqual(project.slug, "renamed-project")

    def test_get_absolute_url(self):
        url = self.project.get_absolute_url()
        self.assertIn(self.project.slug, url)

    def test_active_manager_excludes_inactive(self):
        Project(**{**self.BASE, "name": "Inactive Project", "active": False}).save(clean=False)
        names = list(Project.active_projects.values_list("name", flat=True))
        self.assertNotIn("Inactive Project", names)
        self.assertIn("My Portfolio", names)

    def test_normalize_strips_whitespace(self):
        project = Project(**{**self.BASE, "name": "  Spaced Project  "})
        project.save(clean=False)
        self.assertEqual(project.name, "Spaced Project")
