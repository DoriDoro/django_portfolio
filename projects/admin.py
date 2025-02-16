from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from projects.models import Project, Link, Picture, Skill, Tag


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ["title", "legend", "create_date", "evaluation_date", "published"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Link)
class LinkAdmin(TranslationAdmin):
    list_display = ["title", "origin", "platform", "url", "published"]


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ["legend", "photo", "cover_picture", "published"]
    prepopulated_fields = {"slug": ["legend"]}


@admin.register(Skill)
class SkillAdmin(TranslationAdmin):
    list_display = ["name", "category", "published"]
    list_filter = ["category", "published"]
    list_per_page = 30


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["tag", "published"]
