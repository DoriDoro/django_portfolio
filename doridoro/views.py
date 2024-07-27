from django.views.generic import TemplateView

from doridoro.models import DoriDoro, Job, SocialMedia, Fact, Hobby, Achievement
from projects.models import Project, Tag


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doridoro"] = DoriDoro.objects.first()
        context["social_media"] = SocialMedia.objects.all()
        context["facts"] = Fact.objects.filter(published=True).values_list(
            "content", flat=True
        )
        return context


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["doridoro"] = DoriDoro.objects.first()
        context["current_positions"] = Job.objects.filter(until_present=True)
        context["projects_count"] = Project.objects.filter(published=True).count()
        context["skills_count"] = Tag.objects.filter(published=True)
        context["achievements"] = Achievement.objects.filter(
            published=True
        ).values_list("content", flat=True)
        context["hobbies"] = Hobby.objects.filter(published=True)

        return context


class SkillsView(TemplateView):
    template_name = "skills.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["doridoro"] = DoriDoro.objects.first()
        context["programming_skills"] = self.get_tags_data().filter(
            category=Tag.PROGRAMMING_SKILLS
        )
        context["soft_skills"] = self.get_tags_data().filter(category=Tag.SOFT_SKILLS)
        context["other_skills"] = self.get_tags_data().filter(category=Tag.OTHER)
        context["strength"] = self.get_tags_data().filter(category=Tag.STRENGTH)
        context["weaknesses"] = self.get_tags_data().filter(category=Tag.WEAKNESSES)

        return context

    def get_tags_data(self):
        return Tag.objects.filter(published=True)


class ResumeView(TemplateView):
    template_name = "resume.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["doridoro"] = DoriDoro.objects.first()
        context["jobs_formation"] = (
            self.get_job_data()
            .filter(job_type=Job.FORMATION)
            .order_by("-until_present", "-start_date")
        )
        context["jobs_mentoring"] = (
            self.get_job_data()
            .filter(job_type=Job.MENTORING)
            .order_by("-until_present", "-start_date")
        )
        context["jobs_experience"] = self.get_job_data().filter(
            job_type__in=[
                Job.FREELANCE,
                Job.EMPLOYED,
                Job.APPRENTICESHIP,
                Job.PARENTAL_LEAVE,
                Job.SABBATICAL,
            ]
        )
        return context

    def get_job_data(self):
        return Job.objects.all()
