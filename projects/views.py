from django.views.generic import DetailView, ListView

from projects.models import Project, Link


class PortfolioView(ListView):
    model = Project
    template_name = "portfolio.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.projects_published.order_by("-create_date")
        return context


class PortfolioDetailView(DetailView):
    model = Project
    template_name = "portfolio_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        links = self.object.links.filter(published=True)
        context["githubs"] = links.filter(origin=Link.OriginChoices.GITHUB)
        context["vercels"] = links.filter(origin=Link.OriginChoices.VERCEL)
        context["renders"] = links.filter(origin=Link.OriginChoices.RENDER)
        context["others"] = links.filter(origin=Link.OriginChoices.OTHER)

        return context
