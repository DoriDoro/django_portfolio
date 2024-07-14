import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from projects.models import Link


class Command(BaseCommand):
    help = "This command creates all Link instances for DoriDoro."

    def get_links(self, path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                links = data["links"]

                for link in links:
                    link["origin"] = getattr(Link, link["origin"])
                    link["platform"] = getattr(Link, link["platform"])

                return links

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"The file {path} was not found."))
        except IOError:
            self.stdout.write(
                self.style.ERROR(
                    f"An error occurred while trying to read the file {path}."
                )
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f"The file {path} does not contain valid JSON.")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
        return None

    def handle(self, *args, **options):
        path = "doridoro/management/commands/data.json"

        links = self.get_links(path)
        if links is None:
            return None

        if Link.objects.exists():
            self.stdout.write(
                self.style.WARNING("These instances of Link exists already!")
            )
            return

        try:
            with transaction.atomic():
                for link in links:
                    Link.objects.create(**link)

            self.stdout.write(
                self.style.SUCCESS("Instances of Link successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Link instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
