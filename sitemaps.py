from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from journal.models import Journal
from projects.models import Project


class ProjectSitemap(Sitemap):
    """Sitemap entries for all active projects."""

    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return Project.active_projects.all()


class JournalSitemap(Sitemap):
    """Sitemap entries for all active published journal entries, with lastmod from updated."""

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Journal.active_published_journals.all()

    def lastmod(self, obj):
        return obj.updated


class StaticViewSitemap(Sitemap):
    """Sitemap entries for static pages: about, skills, and resume."""

    priority = 1.0
    changefreq = "yearly"

    def items(self):
        return ["doridoro:about", "doridoro:skills", "doridoro:resume"]

    def location(self, item):
        return reverse(item)
