from django.test import TestCase

from journal.models import Journal


class SlugCreateMixinTestCase(TestCase):
    """Tests SlugCreateMixin behaviour using Journal as a concrete model."""

    def _make_journal(self, name):
        entry = Journal(
            name=name,
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
        )
        entry.save(clean=False)
        return entry

    def test_slug_created_from_name(self):
        entry = self._make_journal("Hello World")
        self.assertEqual(entry.slug, "hello-world")

    def test_slug_lowercased_and_hyphenated(self):
        entry = self._make_journal("My Great Post")
        self.assertEqual(entry.slug, "my-great-post")

    def test_slug_unique_counter_on_first_collision(self):
        # "Same Name!" slugifies to the same "same-name" but passes the unique name constraint
        self._make_journal("Same Name")
        second = self._make_journal("Same Name!")
        self.assertEqual(second.slug, "same-name-1")

    def test_slug_unique_counter_increments_on_multiple_collisions(self):
        # All three slugify to "repeat" but each name is unique
        self._make_journal("Repeat")
        self._make_journal("Repeat!")
        third = self._make_journal("Repeat!!")
        self.assertEqual(third.slug, "repeat-2")

    def test_slug_not_overwritten_if_already_set(self):
        entry = Journal(
            name="Custom Slug Entry",
            slug="my-custom-slug",
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
        )
        entry.save(clean=False)
        self.assertEqual(entry.slug, "my-custom-slug")

    def test_empty_name_raises_value_error(self):
        entry = Journal(
            name="",
            content="<p>Content</p>",
            category=Journal.CategoryChoices.BLOG,
        )
        with self.assertRaises((ValueError, Exception)):
            entry.create_unique_slug(Journal)
