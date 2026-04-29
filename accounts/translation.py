from modeltranslation.translator import register, TranslationOptions

from accounts.models import Profile


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = (
        "phone_number",
        "address",
        "profession",
        "motto",
        "introduction",
        "more_details",
    )
