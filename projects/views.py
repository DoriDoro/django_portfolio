from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView

from projects.models import Project


class PortfolioView(TemplateView):
    template_name = "portfolio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["projects"] = Project.objects.all()
        return context


class PortfolioDetailView(DetailView):
    model = Project
    template_name = "portfolio_details.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        print("000 ", pk)
        return get_object_or_404(Project, pk=pk)

    def get_context_data(self, **kwargs):
        pass
