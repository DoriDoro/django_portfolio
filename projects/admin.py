from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from projects.models import Project, Link, Picture, Skill
from utils.admin.actions import make_active, make_inactive


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ["name", "legend", "active"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["title", "origin", "platform", "url", "active"]
    list_filter = ["platform", "active"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ["title", "picture", "cover_picture", "active"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]
    readonly_fields = ("slug",)

    fields = ("title", "slug", "picture", "cover_picture", "active", "project")


@admin.register(Skill)
class SkillAdmin(TranslationAdmin):
    list_display = ["name", "category", "active"]
    list_filter = ["category", "active"]
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
    list_per_page = 20
    actions = [make_active, make_inactive]
