from django.urls import path

from core.views import ContactView, PortfolioView

app_name = "core"

urlpatterns = [
    path("portfolio/", PortfolioView.as_view(), name="portfolio"),
    path("contact/", ContactView.as_view(), name="contact"),
]
