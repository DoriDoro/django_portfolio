from django.urls import path

from doridoro.views import AboutView, IndexView, ResumeView

app_name = "doridoro"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("resume/", ResumeView.as_view(), name="resume"),
]
