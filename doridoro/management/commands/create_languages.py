from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Language


class Command(BaseCommand):
    help = "This command creates all Language instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            languages = [
                {
                    "name": "German",
                    "level": Language.NATIVE,
                },
                {
                    "name": "English",
                    "level": Language.C1,
                },
                {
                    "name": "French",
                    "level": Language.B2,
                },
            ]

            if Language.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Language exists already!")
                )
                return

            with transaction.atomic():
                for language in languages:
                    Language.objects.create(**language)

            self.stdout.write(
                self.style.SUCCESS("Instances of Language successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Language instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
