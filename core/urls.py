from django.urls import path

from core.views import PortfolioView, ContactView

app_name = "core"

urlpatterns = [
    path("portfolio/", PortfolioView.as_view(), name="portfolio"),
    # path("contact/", ContactView.as_view(), name="contact"),
]
