from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Hobby


class Command(BaseCommand):
    help = "This command creates all Hobby instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            hobbies = [
                {
                    "name": {
                        "en": "dogs",
                        "de": "Hunde",
                        "fr": "chiens",
                    }
                },
                {
                    "name": {
                        "en": "horses",
                        "de": "Pferde",
                        "fr": "cheveaux",
                    }
                },
                {"name": {"en": "handicraft", "de": "Handwerk", "fr": "artisanat"}},
                {"name": {"en": "yoga", "de": "Yoga", "fr": "yoga"}},
                {"name": {"en": "learning", "de": "Lernen", "fr": "apprendre"}},
                {"name": {"en": "hiking", "de": "Wandern", "fr": "randonnée"}},
                {"name": {"en": "biking", "de": "Radfahren", "fr": "vélo"}},
                {"name": {"en": "movies", "de": "Filme", "fr": "films"}},
            ]

            if Hobby.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Hobby exists already!")
                )
                return

            with transaction.atomic():
                for hobby in hobbies:
                    Hobby.objects.create(
                        name_en=hobby["name"]["en"],
                        name_de=hobby["name"]["de"],
                        name_fr=hobby["name"]["fr"],
                    )

            self.stdout.write(
                self.style.SUCCESS("Instances of Hobby successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Hobby instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
