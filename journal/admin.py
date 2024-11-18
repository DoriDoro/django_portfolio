from django.contrib import admin

from journal.models import Journal, Link, Platform, Category


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ["title", "name", "category", "author", "publish", "status"]
    list_filter = ["status", "name", "category", "created", "publish", "author"]
    search_fields = ["title", "name", "category"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish"
    ordering = ["status", "publish"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["title", "platform", "url", "published"]
    search_fields = ["title", "platform__name"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    show_facets = admin.ShowFacets.ALWAYS
