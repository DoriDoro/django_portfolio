from django.core.management.base import BaseCommand
from django.db import IntegrityError

from projects.models import Skill
from utils.management.read_json import read_json_file


class Command(BaseCommand):
    help = "This command creates all Skill instances for DoriDoro."

    def handle(self, *args, **options):
        path = "projects/management/commands/data/projects_data.json"
        data = read_json_file(json_path=path)
        skill_data = data["Skills"]

        try:
            for skill in skill_data:
                name = skill["name"]
                content = skill.get("content", {})
                Skill.objects.create(
                    name_en=name["en"],
                    name_de=name.get("de", ""),
                    name_fr=name.get("fr", ""),
                    category=skill["category"],
                    sub_category=skill.get("sub_category", ""),
                    content_en=content.get("en", ""),
                    content_de=content.get("de", ""),
                    content_fr=content.get("fr", ""),
                )

                self.stdout.write(
                    self.style.SUCCESS(f"Skill: '{name['en']}' successfully created!")
                )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    "[IntegrityError] - These Skill instances exists already!"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"[ERROR] -Skill - An unexpected error occurred: {e}")
            )
