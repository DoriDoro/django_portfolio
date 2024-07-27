from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from projects.models import Project, Tag, Picture, Link

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
    list_display = ["title", "create_date", "published"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Picture)
class PictureAdmin(TranslationAdmin):
    list_display = ["legend", "photo", "published"]
    prepopulated_fields = {"slug": ["legend"]}


@admin.register(Link)
class LinkAdmin(TranslationAdmin):
    list_display = ["title", "origin", "platform", "url", "published"]


@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    list_display = ["name", "category", "published"]
