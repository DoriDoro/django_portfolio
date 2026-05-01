from django.core.management.base import BaseCommand

from projects.models import Skill
from utils.management.read_json import read_json_file


class Command(BaseCommand):
    help = "This command creates all Skill instances."

    def handle(self, *args, **options):
        path = "projects/management/commands/data/projects_data.json"
        data = read_json_file(json_path=path)
        skill_data = data["Skills"]

        for entry in skill_data:
            fields = entry["fields"]
            try:
                skill, created = Skill.objects.get_or_create(
                    name=fields["name_en"],
                    category=fields["category"],
                    sub_category=fields.get("sub_category", ""),
                    defaults={
                        "name_de": fields.get("name_de", ""),
                        "name_fr": fields.get("name_fr", ""),
                        "display_skill": fields.get("display_skill", False),
                        "content_en": fields.get("content_en", ""),
                        "content_de": fields.get("content_de", ""),
                        "content_fr": fields.get("content_fr", ""),
                    },
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Skill: '{skill.name} ({skill.pk})' successfully created!"
                        )
                    )
                else:
                    self.stdout.write(f"Skipped (exists): '{skill.name} ({skill.pk})'")

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"[ERROR] -Skill - An unexpected error occurred: {e}"
                    )
                )
