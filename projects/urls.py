from django.urls import path

from projects.views import PortfolioListView, PortfolioDetailView

app_name = "projects"

urlpatterns = [
    path("", PortfolioListView.as_view(), name="portfolio"),
    path("<slug:slug>/", PortfolioDetailView.as_view(), name="portfolio-detail"),
]
