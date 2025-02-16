from django.urls import path

from contact.views import ContactRequestView

app_name = "contact"

urlpatterns = [
    path("", ContactRequestView.as_view(), name="contact_me"),
]
