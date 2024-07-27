from modeltranslation.translator import register, TranslationOptions

from projects.models import Project, Picture, Link, Tag


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ("title", "introduction", "content")


@register(Picture)
class PictureTranslationOptions(TranslationOptions):
    fields = ("legend",)


@register(Link)
class LinkTranslationOptions(TranslationOptions):
    fields = ("legend", "origin", "platform")


@register(Tag)
class LinkTranslationOptions(TranslationOptions):
    fields = ("category",)
