from django.views.generic import ListView, DetailView

from journal.models import Journal


class JournalListView(ListView):
    model = Journal
    template_name = "journal.html"
    context_object_name = "entries"
    queryset = Journal.journal_published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_entries"] = self.get_filter_entries()
        return context

    def get_filter_entries(self):
        filter_entries = set()
        for entry in self.queryset.filter(category__name__isnull=False).values_list(
            "category__name", "category__slug"
        ):
            filter_entries.add(entry)
        return filter_entries


class JournalDetailView(DetailView):
    model = Journal
    template_name = "journal_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["platform_links"] = self.get_links()
        return context

    def get_links(self):
        dictionary_links = {}
        for link in self.object.links.all():
            platform_name = link.platform.name
            if platform_name not in dictionary_links:
                dictionary_links[platform_name] = []
            dictionary_links[platform_name].append((link.title, link.url))
        return dictionary_links
