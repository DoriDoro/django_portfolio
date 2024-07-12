from django.urls import path

from doridoro.views import (
    IndexView,
    AboutView,
    SkillsView,
    AchievementsView,
    ResumeView,
)

app_name = "doridoro"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("skills/", SkillsView.as_view(), name="skills"),
    path("achievements/", AchievementsView.as_view(), name="achievements"),
    path("resume/", ResumeView.as_view(), name="resume"),
]
