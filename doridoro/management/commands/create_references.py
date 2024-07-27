from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Reference


class Command(BaseCommand):
    help = "This command creates all Reference instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            references = [
                {
                    "name": "Aurélien MALVÉ",
                    "profession": "Django Mentor",
                    "email": "aurelien.malve@djungo.io",
                    "language": {
                        "en": "French, less English",
                        "de": "Französisch, weniger Englisch",
                        "fr": "Français, moins d'anglais",
                    },
                },
                {
                    "name": "Nicolas CHARTIER",
                    "profession": "OpenClassrooms Mentor",
                    "email": "arctenischloria@gmail.com",
                    "language": {
                        "en": "French and English",
                        "de": "Französisch und English",
                        "fr": "Français et Anglais",
                    },
                },
            ]

            if Reference.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Reference exists already!")
                )
                return

            with transaction.atomic():
                for reference in references:
                    Reference.objects.create(
                        language_en=reference["language"]["en"],
                        language_de=reference["language"]["de"],
                        language_fr=reference["language"]["fr"],
                        **reference,
                    )

            self.stdout.write(
                self.style.SUCCESS("Instances of Reference successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Reference instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
