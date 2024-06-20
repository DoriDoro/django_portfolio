from django.views.generic import TemplateView


class PortfolioView(TemplateView):
    template_name = "portfolio.html"


class ContactView(TemplateView):
    template_name = "contact.html"
