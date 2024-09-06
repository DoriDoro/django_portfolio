from modeltranslation.translator import register, TranslationOptions

from projects.models import Project, Picture, Link, Skill


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ("title", "legend", "introduction", "content")


@register(Picture)
class PictureTranslationOptions(TranslationOptions):
    fields = ("legend",)


@register(Link)
class LinkTranslationOptions(TranslationOptions):
    fields = ("legend",)


@register(Skill)
class SkillTranslationOptions(TranslationOptions):
    fields = ("name",)
