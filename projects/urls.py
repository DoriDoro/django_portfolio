from django.urls import path

from projects.views import PortfolioView, PortfolioDetailView

app_name = "projects"

urlpatterns = [
    path("portfolio/", PortfolioView.as_view(), name="portfolio"),
    path(
        "portfolio/<slug:slug>/", PortfolioDetailView.as_view(), name="portfolio-detail"
    ),
]
