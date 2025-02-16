"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from sitemaps import ProjectSitemap, JournalSitemap, StaticViewSitemap

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("tinymce/", include("tinymce.urls")),
    path("journal/", include("journal.urls", namespace="journal")),
]

sitemaps = {
    "projects": ProjectSitemap,
    "journals": JournalSitemap,
    "static": StaticViewSitemap,
}

# translation enables urlpatterns:
urlpatterns += i18n_patterns(
    path("", include("core.urls", namespace="core")),
    path("", include("doridoro.urls", namespace="doridoro")),
    path("portfolio/", include("projects.urls", namespace="projects")),
    path("contact/", include("contact.urls", namespace="contact")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
