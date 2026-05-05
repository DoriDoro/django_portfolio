from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from projects.models import Project, Skill
from utils.admin.actions import make_active, make_inactive


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ["name", "legend", "active"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]


@admin.register(Skill)
class SkillAdmin(TranslationAdmin):
    list_display = ["name", "category", "active"]
    list_filter = ["category", "active"]
    search_fields = ["name"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]
