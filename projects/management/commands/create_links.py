from django.core.management.base import BaseCommand
from django.db import IntegrityError

from projects.models import Link
from utils.management.read_json import read_json_file


class Command(BaseCommand):
    help = "This command creates all Link instances for DoriDoro."

    def handle(self, *args, **options):
        path = "projects/management/commands/data/projects_data.json"
        data = read_json_file(json_path=path)
        link_data = data["Links"]

        try:
            for link in link_data:
                Link.objects.create(**link)

                self.stdout.write(
                    self.style.SUCCESS(f"Link: '{link['title']}' successfully created!")
                )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    "[IntegrityError] - These Link instances exists already!"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"[ERROR] - Link - An unexpected error occurred: {e}")
            )
