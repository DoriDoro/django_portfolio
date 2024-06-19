from django.urls import path

from core.views import ResumeView, PortfolioView, ContactView

app_name = "core"

urlpatterns = [
    path("resume/", ResumeView.as_view(), name="resume"),
    path("portfolio/", PortfolioView.as_view(), name="portfolio"),
    path("contact/", ContactView.as_view(), name="contact"),
]
