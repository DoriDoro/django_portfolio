from django.views.generic import ListView, DetailView

from journal.models import Journal


class JournalListView(ListView):
    model = Journal
    template_name = "journal.html"
    context_object_name = "entries"
    paginate_by = 5


class JournalDetailView(DetailView):
    model = Journal
    template_name = "journal_details.html"
    queryset = Journal.objects.filter(status=Journal.Status.PUBLISHED)
