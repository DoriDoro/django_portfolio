import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from projects.models import Skill


class Command(BaseCommand):
    help = "This command creates all Skill instances for DoriDoro."

    def get_skills(self, path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                skills = data["Skill"]

                for skill in skills:
                    skill["category"] = getattr(Skill.SkillChoices, skill["category"])

            return skills

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"Skill(s) - The file {path} was not found.")
            )
        except IOError:
            self.stdout.write(
                self.style.ERROR(
                    f"Skill(s) - An error occurred while trying to read the file {path}."
                )
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(
                    f"Skill(s) - The file {path} does not contain valid JSON."
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Skill(s) - An unexpected error occurred: {e}")
            )
        return None

    def handle(self, *args, **options):
        path = "projects/management/commands/data_projects.json"

        skills = self.get_skills(path)
        if skills is None:
            return None

        if Skill.objects.exists():
            self.stdout.write(
                self.style.WARNING("These instances of Skill exists already!")
            )
            return

        try:
            with transaction.atomic():
                for skill in skills:
                    Skill.objects.create(
                        name_en=skill["name"],
                        name_de=skill["name"],
                        name_fr=skill["name"],
                        **skill,
                    )

            self.stdout.write(
                self.style.SUCCESS("Instances of Skill successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Skill instances exists already!")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Skill - An unexpected error occurred: {e}")
            )
