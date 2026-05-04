from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.action(description=_("Mark selected as active"))
def make_active(modeladmin, request, queryset):
    updated = queryset.update(active=True)
    modeladmin.message_user(request, _("%d item(s) marked as active.") % updated)


@admin.action(description=_("Mark selected as inactive"))
def make_inactive(modeladmin, request, queryset):
    updated = queryset.update(active=False)
    modeladmin.message_user(request, _("%d item(s) marked as inactive.") % updated)
