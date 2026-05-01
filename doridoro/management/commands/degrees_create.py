from django.core.management.base import BaseCommand
from django.db import IntegrityError

from doridoro.models import Degree


class Command(BaseCommand):
    help = "This command creates all Degree instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            degrees = [
                {
                    "organization": "Ironhack Paris",
                    "degree_en": "RNCP Level 6, Bac+3",
                    "degree_de": "RNCP Level 6, Bac+3",
                    "degree_fr": "RNCP Niveau 6, Bac+3",
                },
                {
                    "organization": "OpenClassrooms",
                    "degree_en": "RNCP Level 6, Bac+4",
                    "degree_de": "RNCP Level 6, Bac+4",
                    "degree_fr": "RNCP Niveau 6, Bac+4",
                },
            ]

            if Degree.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Degree exists already!")
                )
                return

            for degree in degrees:
                Degree.objects.create(**degree)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Degree: '{degree["organization"]}' successfully created!"
                    )
                )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    "[IntegrityError] - These Degree instances exists already!"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"[ERROR] - An unexpected error occurred: {e}")
            )
