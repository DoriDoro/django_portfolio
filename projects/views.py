from django.db.models import Case, CharField, Prefetch, Value, When
from django.db.models.functions import Lower
from django.views.generic import DetailView, ListView

from journal.models import Link
from projects.models import Project, Skill

# -- View Constants --
TAG_NAMES = {"OPENCLASSROOMS": "OpenClassrooms Project", "PERSONAL": "Personal Project"}


class PortfolioListView(ListView):
    model = Project
    template_name = "portfolio.html"
    context_object_name = "projects"

    def get_queryset(self):
        return (
            Project.active_projects.annotate(
                tag_display=Case(
                    *[When(tag=k, then=Value(v)) for k, v in TAG_NAMES.items()],
                    default=Value(""),
                    output_field=CharField()
                )
            )
            .only("id", "name", "slug", "tag", "picture", "create_date")
            .order_by("-create_date")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        seen = dict.fromkeys(e.tag for e in ctx["projects"])
        ctx["filter_tags"] = [Project.TagChoices(t).label for t in seen]
        return ctx


class PortfolioDetailView(DetailView):
    model = Project
    template_name = "portfolio_details.html"
    context_object_name = "project"

    def get_queryset(self):
        prefetch_links = Prefetch(
            "links",
            queryset=Link.active_links.filter(panel=Link.PanelChoices.PROJECT)
            .only("id", "title", "url")
            .order_by(Lower("title"), "pk"),
            to_attr="links_list",
        )
        prefetch_skills = Prefetch(
            "skills",
            queryset=Skill.active_skills.only("id", "name").order_by(Lower("name")),
        )

        return (
            Project.active_projects.prefetch_related(prefetch_links, prefetch_skills)
            .annotate(
                tag_display=Case(
                    *[When(tag=k, then=Value(v)) for k, v in TAG_NAMES.items()],
                    default=Value(""),
                    output_field=CharField()
                )
            )
            .only(
                "id",
                "name",
                "create_date",
                "evaluation_date",
                "introduction",
                "skill_set",
                "experience",
                "future",
            )
            .order_by()
        )
