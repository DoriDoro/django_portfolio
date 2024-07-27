import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from projects.models import Tag


class Command(BaseCommand):
    help = "This command creates all Tag instances for DoriDoro."

    def get_tags(self, path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                tags = data["Tag"]

                for tag in tags:
                    tag["category"] = getattr(Tag, tag["category"])

            return tags

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"Tag(s) - The file {path} was not found.")
            )
        except IOError:
            self.stdout.write(
                self.style.ERROR(
                    f"Tag(s) - An error occurred while trying to read the file {path}."
                )
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(
                    f"Tag(s) - The file {path} does not contain valid JSON."
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Tag(s) - An unexpected error occurred: {e}")
            )
        return None

    def handle(self, *args, **options):
        path = "projects/management/commands/data_projects.json"

        tags = self.get_tags(path)
        if tags is None:
            return None

        if Tag.objects.exists():
            self.stdout.write(
                self.style.WARNING("These instances of Tag exists already!")
            )
            return

        try:
            with transaction.atomic():
                for tag in tags:
                    Tag.objects.create(
                        category_en=tag["category"],
                        category_de=tag["category"],
                        category_fr=tag["category"],
                        **tag,
                    )

            self.stdout.write(
                self.style.SUCCESS("Instances of Tag successfully created!")
            )

        except IntegrityError:
            self.stdout.write(self.style.WARNING("These Tag instances exists already!"))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Tag - An unexpected error occurred: {e}")
            )
