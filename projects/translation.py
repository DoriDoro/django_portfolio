from modeltranslation.translator import register, TranslationOptions

from projects.models import Project, Skill


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ("name", "skill_set", "introduction", "experience", "future")


@register(Skill)
class SkillTranslationOptions(TranslationOptions):
    fields = ("name",)
