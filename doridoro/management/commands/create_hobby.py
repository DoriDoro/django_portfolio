from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Hobby


class Command(BaseCommand):
    help = "This command creates all Hobby instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            hobbies = [
                {"name": "dogs"},
                {"name": "horses"},
                {"name": "handicraft"},
            ]

            if Hobby.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Hobby exists already!")
                )
                return

            with transaction.atomic():
                for hobby in hobbies:
                    Hobby.objects.create(name=hobby["name"])

            self.stdout.write(
                self.style.SUCCESS("Instances of Hobby successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Hobby instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
