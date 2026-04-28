from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.defaults import permission_denied, page_not_found, server_error

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
    urlpatterns += [
        path(
            "__preview__/403/",
            permission_denied,
            {"exception": Exception("Preview 403")},
        ),
        path(
            "__preview__/404/", page_not_found, {"exception": Exception("Preview 404")}
        ),
        path("__preview__/500/", server_error),
    ]
