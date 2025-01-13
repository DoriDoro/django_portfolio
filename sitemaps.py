from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from journal.models import Journal
from projects.models import Project


class ProjectSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return Project.projects_published.all()


class JournalSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Journal.journal_published.all()

    def lastmod(self, obj):
        return obj.updated


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "yearly"

    def items(self):
        return ["doridoro:about", "doridoro:skills", "doridoro:resume"]

    def location(self, item):
        return reverse(item)
