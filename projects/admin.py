from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from projects.models import Project, Link, Picture, Skill, Tag


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ["title", "legend", "create_date", "evaluation_date", "active"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Link)
class LinkAdmin(TranslationAdmin):
    list_display = ["title", "origin", "platform", "url", "active"]


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ["legend", "photo", "cover_picture", "active"]
    prepopulated_fields = {"slug": ["legend"]}


@admin.register(Skill)
class SkillAdmin(TranslationAdmin):
    list_display = ["name", "category", "active"]
    list_filter = ["category", "active"]
    list_per_page = 30


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["tag", "active"]
