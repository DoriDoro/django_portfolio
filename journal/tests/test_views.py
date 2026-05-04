from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate

from journal.models import Journal, Link, Platform


class JournalViewsBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.published = Journal(
            name="A Published Post",
            content="<p>Content here</p>",
            category=Journal.CategoryChoices.BLOG,
            status=Journal.StatusChoices.PUBLISHED,
            published=timezone.now(),
        )
        cls.published.save(clean=False)

        cls.draft = Journal(
            name="A Draft Post",
            content="<p>Draft content</p>",
            category=Journal.CategoryChoices.BLOG,
            status=Journal.StatusChoices.DRAFT,
        )
        cls.draft.save(clean=False)

    def setUp(self):
        activate("en")


class JournalListViewTestCase(JournalViewsBase):
    def test_get_returns_200(self):
        response = self.client.get(reverse("journal:journal"))
        self.assertEqual(response.status_code, 200)

    def test_uses_journal_template(self):
        response = self.client.get(reverse("journal:journal"))
        self.assertTemplateUsed(response, "journal.html")

    def test_only_published_entries_shown(self):
        response = self.client.get(reverse("journal:journal"))
        names = [e.name for e in response.context["entries"]]
        self.assertIn("A Published Post", names)
        self.assertNotIn("A Draft Post", names)

    def test_context_has_filter_categories(self):
        response = self.client.get(reverse("journal:journal"))
        self.assertIn("filter_categories", response.context)

    def test_inactive_entry_not_shown(self):
        Journal(
            name="Inactive Published",
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
            status=Journal.StatusChoices.PUBLISHED,
            published=timezone.now(),
            active=False,
        ).save(clean=False)
        response = self.client.get(reverse("journal:journal"))
        names = [e.name for e in response.context["entries"]]
        self.assertNotIn("Inactive Published", names)


class JournalDetailViewTestCase(JournalViewsBase):
    def test_get_published_returns_200(self):
        url = reverse("journal:journal-detail", kwargs={"slug": self.published.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_uses_detail_template(self):
        url = reverse("journal:journal-detail", kwargs={"slug": self.published.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "journal_details.html")

    def test_context_has_entry(self):
        url = reverse("journal:journal-detail", kwargs={"slug": self.published.slug})
        response = self.client.get(url)
        self.assertEqual(response.context["entry"].name, "A Published Post")

    def test_draft_returns_404(self):
        url = reverse("journal:journal-detail", kwargs={"slug": self.draft.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_inactive_entry_returns_404(self):
        inactive = Journal(
            name="Gone Entry",
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
            status=Journal.StatusChoices.PUBLISHED,
            published=timezone.now(),
            active=False,
        )
        inactive.save(clean=False)
        url = reverse("journal:journal-detail", kwargs={"slug": inactive.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_links_prefetched(self):
        platform = Platform(name="TestPlatform")
        platform.save(clean=False)
        link = Link(
            title="A Link",
            url="https://example.com",
            panel=Link.PanelChoices.JOURNAL,
            platform=platform,
        )
        link.save(clean=False)
        self.published.links.add(link)

        url = reverse("journal:journal-detail", kwargs={"slug": self.published.slug})
        response = self.client.get(url)
        self.assertIn("A Link", [link.title for link in response.context["entry"].links_list])
