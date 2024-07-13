from django.contrib import admin

from doridoro.models import (
    DoriDoro,
    Achievement,
    Degree,
    Fact,
    Hobby,
    Job,
    Language,
    Reference,
    SocialMedia,
    Website,
)


@admin.register(DoriDoro)
class DoriDoroAdmin(admin.ModelAdmin):
    list_display = ["address", "profession"]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ["title", "published"]


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ["organization", "degree", "published"]


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ["title", "published"]


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ["name", "published"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "position",
        "start_date",
        "until_present",
        "job_type",
        "published",
    ]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name", "level", "published"]


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ["name", "published"]


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ["name", "published"]


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ["name", "published"]
