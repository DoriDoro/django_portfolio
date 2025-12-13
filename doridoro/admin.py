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
    list_display = ["title", "content", "active"]


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ["organization", "degree", "url", "active"]


@admin.register(Fact)
class FactAdmin(TranslationAdmin):
    list_display = ["title", "content", "active"]


@admin.register(Hobby)
class HobbyAdmin(TranslationAdmin):
    list_display = ["name", "active"]


@admin.register(Job)
class JobAdmin(TranslationAdmin):
    list_display = [
        "position",
        "company_name",
        "start_date",
        "until_present",
        "job_type",
        "active",
    ]


@admin.register(Language)
class LanguageAdmin(TranslationAdmin):
    list_display = ["name", "level", "active"]


@admin.register(Reference)
class ReferenceAdmin(TranslationAdmin):
    list_display = ["name", "email", "active"]


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "active"]
