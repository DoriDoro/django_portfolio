from django.urls import path

from journal.views import JournalListView, JournalDetailView

app_name = "journal"

urlpatterns = [
    path("", JournalListView.as_view(), name="journal"),
    path("<slug:slug>/", JournalDetailView.as_view(), name="journal-detail"),
]
