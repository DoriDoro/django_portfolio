from modeltranslation.translator import register, TranslationOptions

from doridoro.models import (
    DoriDoro,
    Achievement,
    Degree,
    Fact,
    Hobby,
    Job,
    Language,
    Reference,
)


@register(DoriDoro)
class DoriDoroTranslationOptions(TranslationOptions):
    fields = (
        "phone",
        "address",
        "profession",
        "introduction",
        "dream_job",
        "free_time",
    )


@register(Achievement)
class AchievementTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(Degree)
class DegreeTranslationOptions(TranslationOptions):
    fields = ("degree",)


@register(Fact)
class FactTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(Hobby)
class HobbyTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Job)
class JobTranslationOptions(TranslationOptions):
    fields = ("company_name", "position", "address", "job_type", "description")


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Reference)
class ReferenceTranslationOptions(TranslationOptions):
    fields = ("language",)
