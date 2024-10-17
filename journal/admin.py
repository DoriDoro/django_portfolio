from django.contrib import admin

from journal.models import Journal


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish"
    ordering = ["status", "publish"]
    show_facets = admin.ShowFacets.ALWAYS
