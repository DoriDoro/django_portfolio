import logging

from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from accounts.models import Profile
from doridoro.models import Achievement, Job, Language, SocialMedia
from projects.models import Project, Skill

logger = logging.getLogger(__name__)


# -- View Constants --
PORTFOLIO_USERNAME = "Doro"


class IndexView(TemplateView):
    """Home page; shows the owner's profession and social media links."""

    template_name = "index.html"

    @cached_property
    def profile(self):
        return get_object_or_404(
            Profile.objects.select_related("user").only(
                "id", "profession", "user__id", "user__first_name", "user__last_name"
            ),
            user__username=PORTFOLIO_USERNAME,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["doridoro"] = self.profile
        ctx["social_media"] = SocialMedia.active_social_medias.values_list("name", "url")
        return ctx


class AboutView(TemplateView):
    """About page; shows profile details, current positions, and summary stats."""

    template_name = "about.html"

    @cached_property
    def profile(self):
        return get_object_or_404(
            Profile.objects.select_related("user").only(
                "id",
                "phone_number",
                "address",
                "profession",
                "introduction",
                "user__id",
                "user__email",
            ),
            user__username=PORTFOLIO_USERNAME,
        )

    @cached_property
    def jobs(self):
        return Job.active_jobs.filter(until_present=True).values_list("position", "company_name")

    @cached_property
    def project_count(self):
        return Project.active_projects.count()

    @cached_property
    def skill_count(self):
        return Skill.active_skills.count()

    @cached_property
    def achievements(self):
        return Achievement.active_achievements.values_list("title", "content")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["doridoro"] = self.profile
        ctx["current_positions"] = self.jobs
        ctx["projects_count"] = self.project_count
        ctx["skills_count"] = self.skill_count
        ctx["achievements"] = self.achievements
        return ctx


class SkillsView(TemplateView):
    """Skills page; groups skills by category and lists spoken languages."""

    template_name = "skills.html"

    @cached_property
    def skills_qs(self):
        return Skill.display_active_skills.only(
            "id", "name", "category", "sub_category", "content"
        ).order_by(Lower("name"), "pk")

    @cached_property
    def profile(self):
        return get_object_or_404(
            Profile.objects.only("id", "motto", "more_details"),
            user__username="Doro",
        )

    # -- Helpers --
    def _get_languages_data(self):
        languages = Language.active_languages.only("id", "name", "level").order_by("-level")
        return [(lang.name, lang.get_level_display()) for lang in languages]

    def _create_skills_context(self):
        all_skills = list(self.skills_qs)
        programming_skills, soft_skills, strength = {}, [], []

        for skill in all_skills:
            if skill.category == Skill.CategoryChoices.PROGRAMMING_SKILLS:
                programming_skills.setdefault(skill.get_sub_category_display(), []).append(
                    skill.name
                )
            elif skill.category == Skill.CategoryChoices.SOFT_SKILLS:
                soft_skills.append(skill.name)
            elif skill.category == Skill.CategoryChoices.STRENGTH:
                strength.append((skill.name, skill.content))

        return {
            "programming_skills": programming_skills,
            "soft_skills": soft_skills,
            "strength": strength,
            "languages": self._get_languages_data(),
        }

    # -- Methods --
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["doridoro"] = self.profile
        ctx.update(self._create_skills_context())
        return ctx


class ResumeView(TemplateView):
    """Resume page; splits jobs into formation, mentoring, and experience groups."""

    template_name = "resume.html"

    @cached_property
    def jobs(self):
        return Job.active_jobs.only(
            "id",
            "company_name",
            "address",
            "position",
            "description",
            "job_type",
            "work_type",
            "start_date",
            "end_date",
            "until_present",
        ).order_by("-start_date", "pk")

    def _create_jobs_context(self):
        all_jobs = list(self.jobs)
        formation_types = {Job.JobTypeChoices.FORMATION, Job.JobTypeChoices.MENTORING}
        formation, mentoring, experience = [], [], []

        for job in all_jobs:
            if job.job_type == Job.JobTypeChoices.FORMATION:
                formation.append(job)
            elif job.job_type == Job.JobTypeChoices.MENTORING:
                mentoring.append(job)
            elif job.job_type not in formation_types:
                experience.append(job)

        return {
            "jobs_formation": formation,
            "jobs_mentoring": mentoring,
            "jobs_experience": experience,
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self._create_jobs_context())
        return ctx
