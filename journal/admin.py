from django.contrib import admin

from journal.models import Journal, Link, Platform, Category


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ["name", "category__name", "published", "status", "active"]
    list_filter = ["status", "name", "category__name", "created", "published"]
    search_fields = ["name"]
    date_hierarchy = "published"
    ordering = ["status", "-published"]
    list_per_page = 20
    show_facets = admin.ShowFacets.ALWAYS
    readonly_fields = ("slug",)

    fields = [
        "name",
        "slug",
        "status",
        "content",
        "published",
        "active",
        "created_by",
        "category",
        "links",
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    search_fields = ["name"]
    list_per_page = 20
    show_facets = admin.ShowFacets.ALWAYS
    readonly_fields = ("slug",)

    fields = ["name", "slug", "active"]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["title", "platform", "url", "active"]
    list_filter = ["platform"]
    search_fields = ["title", "platform__name"]
    date_hierarchy = "created"
    list_per_page = 20
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    search_fields = ["name"]
    list_per_page = 20
    show_facets = admin.ShowFacets.ALWAYS
    readonly_fields = ("slug",)

    fields = ["name", "slug"]
