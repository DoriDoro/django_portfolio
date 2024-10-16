from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

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
)


@admin.register(DoriDoro)
class DoriDoroAdmin(TranslationAdmin):
    list_display = ["phone", "address", "profession"]


@admin.register(Achievement)
class AchievementAdmin(TranslationAdmin):
    list_display = ["title", "content", "published"]


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ["organization", "degree", "url", "published"]


@admin.register(Fact)
class FactAdmin(TranslationAdmin):
    list_display = ["title", "content", "published"]


@admin.register(Hobby)
class HobbyAdmin(TranslationAdmin):
    list_display = ["name", "published"]


@admin.register(Job)
class JobAdmin(TranslationAdmin):
    list_display = [
        "position",
        "company_name",
        "start_date",
        "until_present",
        "job_type",
        "published",
    ]


@admin.register(Language)
class LanguageAdmin(TranslationAdmin):
    list_display = ["name", "level", "published"]


@admin.register(Reference)
class ReferenceAdmin(TranslationAdmin):
    list_display = ["name", "email", "published"]


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "published"]
