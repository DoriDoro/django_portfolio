from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from projects.models import Project, Link, Picture, Skill, Tag

"""
    #list display
    list_display = ['name', 'price', 'category', 'date']
    #list Filter
    list_filter = ('category','date') on the right hand side
    # search list
    search_fields = ['name']
"""


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ["title", "legend", "create_date", "evaluation_date", "published"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Link)
class LinkAdmin(TranslationAdmin):
    list_display = ["title", "origin", "platform", "url", "published"]


@admin.register(Picture)
class PictureAdmin(TranslationAdmin):
    list_display = ["legend", "photo", "cover_picture", "published"]
    prepopulated_fields = {"slug": ["legend"]}


@admin.register(Skill)
class SkillAdmin(TranslationAdmin):
    list_display = ["name", "category", "published"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["tag", "published"]
