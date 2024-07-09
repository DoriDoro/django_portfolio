from django.views.generic import DetailView, ListView

from projects.models import Project, Picture


class PortfolioView(ListView):
    model = Project
    template_name = "portfolio.html"  # project_list.html
    context_object_name = "projects"  # use get_context_data() for additional context


class PortfolioDetailView(DetailView):
    model = Project
    template_name = "portfolio_details.html"
    context_object_name = "project"
