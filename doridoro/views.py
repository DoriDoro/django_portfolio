from django.views.generic import TemplateView

from doridoro.models import DoriDoro, Job, SocialMedia, Fact
from projects.models import Project


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doridoro"] = self.get_doridoro_data().first()
        context["social_media"] = self.get_social_media_data()
        context["facts"] = self.get_fact_data()
        return context

    def get_doridoro_data(self):
        return DoriDoro.objects.all()

    def get_social_media_data(self):
        return SocialMedia.objects.all()

    def get_fact_data(self):
        return Fact.objects.values_list("content", flat=True)


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["doridoro"] = self.get_doridoro_data().first()
        context["current_positions"] = self.get_current_position()
        context["projects"] = self.get_projects_data()
        context["projects_count"] = self.get_projects_data().count()
        return context

    def get_doridoro_data(self):
        return DoriDoro.objects.all()

    def get_projects_data(self):
        return Project.objects.all()

    def get_current_position(self):
        return Job.objects.filter(until_present=True)


class ResumeView(TemplateView):
    template_name = "resume.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["doridoro"] = self.get_doridoro_data().first()
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

    def get_doridoro_data(self):
        return DoriDoro.objects.all()

    def get_job_data(self):
        return Job.objects.all()
