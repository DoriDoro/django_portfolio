from django.views.generic import TemplateView

from doridoro.models import DoriDoro, Job
from projects.models import Project


class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["doridoro"] = self.get_doridoro_data().first()
        context["jobs"] = self.get_job_data()
        context["projects"] = self.get_projects_data()
        context["projects_count"] = self.get_projects_data().count()
        return context

    def get_doridoro_data(self):
        return DoriDoro.objects.all()

    def get_projects_data(self):
        return Project.objects.all()

    def get_job_data(self):
        return Job.objects.all()
