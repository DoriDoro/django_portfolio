from django.contrib import admin

from journal.models import Journal, Link, Platform


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ["title", "name", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish"
    ordering = ["status", "publish"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["title", "platform", "url", "published"]
    list_filter = ["title", "platform"]
    search_fields = ["platform", "journal"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    show_facets = admin.ShowFacets.ALWAYS
