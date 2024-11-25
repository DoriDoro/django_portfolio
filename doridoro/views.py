from django.utils.translation import gettext
from django.views.generic import TemplateView

from doridoro.models import (
    DoriDoro,
    Achievement,
    Fact,
    Hobby,
    Job,
    Language,
    SocialMedia,
)
from projects.models import Project, Skill


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doridoro"] = (
            DoriDoro.objects.select_related("user")
            .only("profession", "user__first_name", "user__last_name")
            .first()
        )
        context["social_media"] = SocialMedia.objects.filter(
            published=True
        ).values_list("name", "url")
        context["facts"] = Fact.objects.filter(published=True).values_list(
            "content", flat=True
        )
        return context


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["doridoro"] = (
            DoriDoro.objects.select_related("user")
            .only(
                "user__email",
                "phone",
                "address",
                "profession",
                "introduction",
                "free_time",
            )
            .first()
        )
        context["current_positions"] = Job.objects.filter(
            until_present=True,
            published=True,
        ).values_list("position", "company_name")
        context["projects_count"] = Project.objects.filter(published=True).count()
        context["skills_count"] = Skill.objects.filter(published=True).count()
        context["achievements"] = Achievement.objects.filter(
            published=True
        ).values_list("content", flat=True)
        context["hobbies"] = Hobby.objects.filter(published=True).values_list(
            "name", flat=True
        )

        return context


class SkillsView(TemplateView):
    template_name = "skills.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["doridoro"] = DoriDoro.objects.values_list(
            "dream_job", flat=True
        ).first()
        context["programming_skills_published"] = self.get_skills_data().filter(
            category=Skill.SkillChoices.PROGRAMMING_SKILLS
        )
        context["soft_skills"] = self.translate_skills_name(
            category=Skill.SkillChoices.SOFT_SKILLS
        )
        context["other_skills_published"] = self.get_skills_data().filter(
            category=Skill.SkillChoices.OTHER
        )
        context["strength"] = self.translate_skills_name(
            category=Skill.SkillChoices.STRENGTH
        )
        context["languages"] = self.get_languages_data()

        return context

    def get_skills_data(self):
        return Skill.objects.filter(published=True).values_list("name", flat=True)

    def translate_skills_name(self, category):
        tags = self.get_skills_data().values_list("name", "category")
        result_dict = {"SOFT_SKILLS": (), "STRENGTH": ()}
        for tag in tags:
            if tag[1] in ["SOFT_SKILLS", "STRENGTH"]:
                translated_name = gettext(tag[0])
                result_dict[tag[1]] += ((translated_name, tag[1]),)

        return result_dict[category]

    def get_languages_data(self):
        languages = Language.objects.all()
        language_tuple = ()
        for language in languages:
            language_tuple += ((language.name, language.get_level_display()),)
        return language_tuple


class ResumeView(TemplateView):
    template_name = "resume.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jobs_formation"] = self.get_job_data().filter(
            job_type=Job.JobType.FORMATION
        )
        context["jobs_mentoring"] = self.get_job_data().filter(
            job_type=Job.JobType.MENTORING
        )
        context["jobs_experience"] = self.get_job_data().filter(
            job_type__in=[
                Job.JobType.FREELANCE,
                Job.JobType.EMPLOYED,
                Job.JobType.APPRENTICESHIP,
                Job.JobType.PARENTAL_LEAVE,
                Job.JobType.SABBATICAL,
            ]
        )
        return context

    def get_job_data(self):
        return (
            Job.objects.filter(published=True)
            .order_by("-until_present", "-start_date")
            .values_list(
                "company_name",
                "position",
                "start_date",
                "end_date",
                "address",
                "description",
            )
        )
