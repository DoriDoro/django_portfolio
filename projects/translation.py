from modeltranslation.translator import register, TranslationOptions

from projects.models import Project, Link, Skill


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ("title", "legend", "keywords", "introduction", "experience", "future")


@register(Link)
class LinkTranslationOptions(TranslationOptions):
    fields = ("legend",)


@register(Skill)
class SkillTranslationOptions(TranslationOptions):
    fields = ("name",)
