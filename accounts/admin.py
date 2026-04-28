from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TranslationAdmin

from accounts.models import Profile

UserModel = get_user_model()

admin.site.register(UserModel, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(TranslationAdmin):
    list_display = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
