from django.views.generic import DetailView, ListView

from projects.models import Project, Link


class PortfolioView(ListView):
    model = Project
    template_name = "portfolio.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(published=True)
        return context


class PortfolioDetailView(DetailView):
    model = Project
    template_name = "portfolio_details.html"
    queryset = Project.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        links = self.object.links.all()
        context["github"] = links.filter(origin=Link.GITHUB, published=True).first()
        context["vercel"] = links.filter(origin="VERCEL", published=True).first()
        context["render"] = links.filter(origin="RENDER", published=True).first()
        context["others"] = links.filter(origin="OTHER", published=True)

        return context
