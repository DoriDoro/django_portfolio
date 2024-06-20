from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Degree, DoriDoro


class Command(BaseCommand):
    help = "This command creates all Degree instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            degrees = [
                {"organization": "Ironhack Paris", "degree": "Bachelor"},
                {"organization": "OpenClassrooms", "degree": "Bachelor"},
            ]

            if Degree.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Degree exists already!")
                )
                return

            with transaction.atomic():
                for degree in degrees:
                    Degree.objects.create(**degree)

            self.stdout.write(
                self.style.SUCCESS("Instances of Degree successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Degree instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
