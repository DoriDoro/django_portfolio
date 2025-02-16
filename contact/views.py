from django.contrib.messages.views import SuccessMessageMixin
from django.db import OperationalError
from django.http import HttpResponse, HttpResponseServerError
from django.urls import reverse_lazy
from django.views.generic import FormView

from contact.forms import ContactRequestForm


class ContactRequestView(SuccessMessageMixin, FormView):
    form_class = ContactRequestForm
    template_name = "contact.html"
    success_message = "Your message was sent."
    success_url = reverse_lazy("doridoro:index")

    def form_valid(self, form):
        try:
            form.save()
            form.send_email()
        except OperationalError as e:
            print("--- Database error - Contact Form ---", e)
            return HttpResponseServerError("Database error: Have you run migrations?")
        except Exception as e:
            print("--- View error - Contact Form ---", e)
            return HttpResponseServerError("An unexpected error occurred.")
        return super().form_valid(form)
