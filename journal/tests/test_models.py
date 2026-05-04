from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from journal.models import Journal, Link, Platform


class PlatformTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.platform = Platform(name="GitHub")
        cls.platform.save(clean=False)

    def test_str(self):
        self.assertEqual(str(self.platform), "GitHub")

    def test_normalize_strips_whitespace(self):
        p = Platform(name="  YouTube  ")
        p.save(clean=False)
        self.assertEqual(p.name, "YouTube")

    def test_duplicate_name_case_insensitive_raises(self):
        dup = Platform(name="github")
        with self.assertRaises(Exception):
            dup.save(clean=False)


class LinkTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.platform = Platform(name="GitHub")
        cls.platform.save(clean=False)
        cls.link = Link(
            title="My Repo",
            url="https://github.com/test/repo",
            panel=Link.PanelChoices.JOURNAL,
            platform=cls.platform,
        )
        cls.link.save(clean=False)

    def test_str(self):
        self.assertEqual(str(self.link), "My Repo")

    def test_normalize_strips_whitespace(self):
        link = Link(
            title="  Trimmed  ",
            url="  https://github.com/test/trimmed  ",
            panel=Link.PanelChoices.JOURNAL,
            platform=self.platform,
        )
        link.save(clean=False)
        self.assertEqual(link.title, "Trimmed")
        self.assertEqual(link.url, "https://github.com/test/trimmed")

    def test_duplicate_platform_url_raises(self):
        dup = Link(
            title="Different Title",
            url="https://github.com/test/repo",
            panel=Link.PanelChoices.JOURNAL,
            platform=self.platform,
        )
        with self.assertRaises(Exception):
            dup.save(clean=False)

    def test_active_manager_excludes_inactive(self):
        Link(
            title="Inactive Link",
            url="https://github.com/test/inactive",
            panel=Link.PanelChoices.JOURNAL,
            platform=self.platform,
            active=False,
        ).save(clean=False)
        titles = list(Link.active_links.values_list("title", flat=True))
        self.assertNotIn("Inactive Link", titles)
        self.assertIn("My Repo", titles)


class JournalTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.journal = Journal(
            name="My First Post",
            content="<p>Hello world</p>",
            category=Journal.CategoryChoices.BLOG,
            status=Journal.StatusChoices.DRAFT,
        )
        cls.journal.save(clean=False)

    def test_str(self):
        self.assertEqual(str(self.journal), "My First Post")

    def test_slug_auto_generated_on_save(self):
        self.assertEqual(self.journal.slug, "my-first-post")

    def test_slug_unique_counter_on_collision(self):
        # "My First Post!" slugifies to the same "my-first-post"
        # but passes the unique name constraint
        second = Journal(
            name="My First Post!",
            content="<p>Hello again</p>",
            category=Journal.CategoryChoices.BLOG,
        )
        second.save(clean=False)
        self.assertEqual(second.slug, "my-first-post-1")

    def test_slug_regenerated_when_name_changes(self):
        entry = Journal(
            name="Original Name",
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
        )
        entry.save(clean=False)
        self.assertEqual(entry.slug, "original-name")

        entry.name = "Updated Name"
        entry.save(clean=False)
        self.assertEqual(entry.slug, "updated-name")

    def test_mark_published_sets_status_and_date(self):
        entry = Journal(
            name="To Be Published",
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
        )
        entry.save(clean=False)
        entry.mark_published()

        entry.refresh_from_db()
        self.assertEqual(entry.status, Journal.StatusChoices.PUBLISHED)
        self.assertIsNotNone(entry.published)

    def test_published_status_without_date_raises(self):
        entry = Journal(
            name="No Date Published",
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
            status=Journal.StatusChoices.PUBLISHED,
            published=None,
        )
        with self.assertRaises(ValidationError):
            entry.validate_constraints()

    def test_active_published_manager_filters_correctly(self):
        Journal(
            name="Published Entry",
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
            status=Journal.StatusChoices.PUBLISHED,
            published=timezone.now(),
        ).save(clean=False)
        Journal(
            name="Draft Entry",
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
            status=Journal.StatusChoices.DRAFT,
        ).save(clean=False)
        Journal(
            name="Inactive Published",
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
            status=Journal.StatusChoices.PUBLISHED,
            published=timezone.now(),
            active=False,
        ).save(clean=False)

        names = list(Journal.active_published_journals.values_list("name", flat=True))
        self.assertIn("Published Entry", names)
        self.assertNotIn("Draft Entry", names)
        self.assertNotIn("Inactive Published", names)

    def test_get_absolute_url(self):
        url = self.journal.get_absolute_url()
        self.assertIn(self.journal.slug, url)
