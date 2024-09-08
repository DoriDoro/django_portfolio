from django.urls import path

from projects.views import PortfolioView, PortfolioDetailView

app_name = "projects"

urlpatterns = [
    path("", PortfolioView.as_view(), name="portfolio"),
    path(
        "<slug:slug>/", PortfolioDetailView.as_view(), name="portfolio-detail"
    ),
]
