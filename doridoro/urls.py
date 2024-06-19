from django.urls import path

from doridoro.views import IndexView, AboutView

app_name = "doridoro"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
]
