from modeltranslation.translator import register, TranslationOptions

from doridoro.models import Achievement, Degree, Job, Language


@register(Achievement)
class AchievementTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(Degree)
class DegreeTranslationOptions(TranslationOptions):
    fields = ("degree",)


@register(Job)
class JobTranslationOptions(TranslationOptions):
    fields = ("position", "address", "description")


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ("name",)
