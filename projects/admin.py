from django.contrib import admin

from projects.models import Project, Tag, Image, Link


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "create_date", "published"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [
        "legend",
    ]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["url", "published"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
