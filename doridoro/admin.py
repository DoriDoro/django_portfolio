from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from doridoro.models import Achievement, Degree, Job, Language, SocialMedia
from utils.admin.actions import make_active, make_inactive


@admin.register(Achievement)
class AchievementAdmin(TranslationAdmin):
    list_display = ["title", "content", "active"]
    list_filter = ["active"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ["organization", "degree", "url", "active"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]


@admin.register(Job)
class JobAdmin(TranslationAdmin):
    list_display = ["position", "company_name", "until_present", "job_type", "active"]
    list_filter = ["active", "job_type"]
    ordering = ["start_date"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]


@admin.register(Language)
class LanguageAdmin(TranslationAdmin):
    list_display = ["name", "level", "active"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "active"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]
