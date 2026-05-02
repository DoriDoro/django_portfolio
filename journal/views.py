from django.db.models import Case, CharField, Prefetch, Value, When
from django.db.models.functions import Lower
from django.views.generic import ListView, DetailView

from journal.models import Journal, Link

# -- View Constants --
CATEGORY_NAMES = {
    "BLOG": "Doro's Python Life in Words Journal",
    "EPIC_EVENTS": "EpicEvents Journal",
    "JOURNAL": "Journal",
    "OC_LETTINGS": "Orange Country Lettings Journal",
    "PORTFOLIO": "Django Portfolio Journal",
    "SOFT_DESK": "SoftDesk Journal",
}


class JournalListView(ListView):
    model = Journal
    template_name = "journal.html"
    context_object_name = "entries"

    # -- Methods --
    def get_queryset(self):
        return (
            Journal.active_published_journals.annotate(
                category_display=Case(
                    *[When(category=k, then=Value(v)) for k, v in CATEGORY_NAMES.items()],
                    default=Value(""),
                    output_field=CharField(),
                )
            )
            .only("id", "name", "slug", "category", "created")
            .order_by("-created", "-pk")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        seen = dict.fromkeys(e.category for e in ctx["entries"])
        ctx["filter_categories"] = [Journal.CategoryChoices(c).label for c in seen]
        return ctx


class JournalDetailView(DetailView):
    model = Journal
    template_name = "journal_details.html"
    context_object_name = "entry"

    # -- Methods --
    def get_queryset(self):
        prefetch_links = Prefetch(
            "links",
            queryset=Link.active_links.select_related("platform")
            .only("id", "title", "url", "platform__id", "platform__name")
            .order_by(Lower("title"), "pk"),
            to_attr="links_list",
        )
        return (
            Journal.active_published_journals.prefetch_related(prefetch_links)
            .annotate(
                category_display=Case(
                    *[When(category=k, then=Value(v)) for k, v in CATEGORY_NAMES.items()],
                    default=Value(""),
                    output_field=CharField(),
                )
            )
            .only("id", "name", "category", "content")
        )
