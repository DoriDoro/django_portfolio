from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db import models

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
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "create_date", "published"]
    prepopulated_fields = {"slug": ["title"]}
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget},
    }


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ["legend", "photo", "published"]
    prepopulated_fields = {"slug": ["legend"]}


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["title", "origin", "platform", "url", "published"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "published"]
