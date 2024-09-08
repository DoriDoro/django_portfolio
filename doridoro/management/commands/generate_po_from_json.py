import json

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command creates django.po files for the JSON data."

    """
    #: doridoro/models.py:13
    msgid "user instance"
    msgstr "Benutzerinstanz"
    """

    def generate_po_file(self, language, translations):
        po_content = []
        po_content.append("#: doridoro/managment/commands/data_doridoro.json")

        for msgid, msgstr in translations.items():
            po_content.append(f'msgid "{msgid}"')
            po_content.append(f'msgstr "{msgstr}"')
            po_content.append("")

        return "\n".join(po_content)

    def get_model_field_names(self, model):
        return [field.name for field in model._meta.get_fields()]

    def get_model_name(self, model_key):
        try:
            return apps.get_model("doridoro", model_key)
        except LookupError:
            self.stdout.write(
                self.style.ERROR(f"Model {model_key} not found in app 'your_app'")
            )
        return None

    def handle(self, *args, **options):
        path = "doridoro/management/commands"

        with open(f"{path}/data_doridoro.json", "r") as file:
            data = json.load(file)
            translations_de = {}
            translations_fr = {}

            for key, content_list in data.items():
                model_name = self.get_model_name(key)
                if not model_name:
                    continue

                fields = self.get_model_field_names(model_name)

                for value in content_list:
                    for field in fields:
                        if field in value:
                            field_content = value[field]
                            if isinstance(field_content, dict):
                                trans_en = field_content.get("en")
                                trans_de = field_content.get("de", None)
                                trans_fr = field_content.get("fr", None)
                                if trans_en and trans_de:
                                    translations_de[trans_en] = trans_de
                                if trans_en and trans_fr:
                                    translations_fr[trans_en] = trans_fr

            po_de_content = self.generate_po_file("de", translations_de)
            po_fr_content = self.generate_po_file("fr", translations_fr)

            with open(f"{path}/django_de.po", "w") as po_de_file:
                po_de_file.write(po_de_content)

            with open(f"{path}/django_fr.po", "w") as po_fr_file:
                po_fr_file.write(po_fr_content)
