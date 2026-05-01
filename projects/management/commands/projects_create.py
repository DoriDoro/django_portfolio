from django.core.management.base import BaseCommand

from journal.models import Link
from projects.models import Project, Skill
from utils.management.read_json import read_json_file


class Command(BaseCommand):
    help = "This command creates all Project instances."

    def handle(self, *args, **options):
        path = "projects/management/commands/data/projects_data.json"
        data = read_json_file(json_path=path)
        project_data = data["Projects"]

        for entry in project_data:
            fields = entry["fields"]
            try:
                project, created = Project.objects.get_or_create(
                    name=fields["name"],
                    defaults={
                        "legend": fields["legend"],
                        "create_date": fields["create_date"],
                        "evaluation_date": fields["evaluation_date"],
                        "skill_set_en": fields["skill_set_en"],
                        "skill_set_de": fields["skill_set_de"],
                        "skill_set_fr": fields["skill_set_fr"],
                        "introduction_en": fields["introduction_en"],
                        "introduction_de": fields["introduction_de"],
                        "introduction_fr": fields["introduction_fr"],
                        "experience_en": fields["experience_en"],
                        "experience_de": fields["experience_de"],
                        "experience_fr": fields["experience_fr"],
                        "future_en": fields["future_en"],
                        "future_de": fields["future_de"],
                        "future_fr": fields["future_fr"],
                        "active": fields["active"],
                        "tag": fields["tag"],
                    },
                )
                if created:
                    for pk in fields.get("links", []):
                        try:
                            project.links.add(Link.objects.get(pk=pk))
                        except Link.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(f"  Link pk={pk} not found, skipped")
                            )
                    for pk in fields.get("skills", []):
                        try:
                            project.skills.add(Skill.objects.get(pk=pk))
                        except Skill.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"  Skill pk={pk} not found, skipped"
                                )
                            )

                    self.stdout.write(
                        self.style.SUCCESS(f"Created: '{project.name} ({project.pk})'")
                    )
                else:
                    self.stdout.write(
                        f"Skipped (exists): '{project.name} ({project.pk})'"
                    )

            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(
                        f"[ERROR] - Project - An unexpected error occurred: {exc}"
                    )
                )
