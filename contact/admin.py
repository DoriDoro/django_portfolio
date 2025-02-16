from django.contrib import admin

from contact.models import ContactRequest, Category


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ["first_name", "subject", "category"]
    list_filter = ["first_name", "email", "subject", "category"]
    search_fields = ["first_name", "email", "subject", "category"]
    date_hierarchy = "submitted_at"
    ordering = ["submitted_at"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]
    ordering = ["created"]
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
