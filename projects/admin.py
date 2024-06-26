from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db import models

from projects.models import Project, Tag, Picture, Link


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "create_date", "published"]
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget},
    }


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ["legend", "photo", "published"]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["url", "published"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
