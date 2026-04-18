from django.contrib import admin

from contact.models import ContactRequest, Category
from utils.admin.actions import make_active, make_inactive


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ["first_name", "subject", "category", "submitted_at"]
    list_filter = ["category__name"]
    search_fields = ["first_name", "email", "subject", "category__name"]
    date_hierarchy = "submitted_at"
    ordering = ["-submitted_at"]
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    search_fields = ["name"]
    ordering = ["name"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]
    readonly_fields = ("slug",)

    fields = ("name", "slug", "active")
