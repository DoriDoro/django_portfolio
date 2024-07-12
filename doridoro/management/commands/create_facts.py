from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Fact


class Command(BaseCommand):
    help = "This command creates all Fact instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            facts = [
                {
                    "title": "Availability",
                    "content": (
                        "I am currently in search of a new job opportunity and am "
                        "available to start within 1.5 months. I am eager to bring my "
                        "skills and experience to a new role and contribute to the "
                        "success of a dynamic organization."
                    ),
                },
                {
                    "title": "Relocate",
                    "content": (
                        "I need to vacate my current apartment by 31.12.2024 and am fully "
                        "prepared to relocate within France, preferably near the German border, "
                        "or to Switzerland. I am open to new opportunities that align "
                        "with this transition."
                    ),
                },
                {
                    "title": "Formation",
                    "content": (
                        "I am currently at the final stage of my formation and will complete it "
                        "upon securing a new employer. I am eager to apply my knowledge and "
                        "skills in a new role and finalize my training with hands-on experience "
                        "in a professional setting."
                    ),
                },
            ]

            if Fact.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Fact exists already!")
                )
                return

            with transaction.atomic():
                for fact in facts:
                    Fact.objects.create(**fact)

            self.stdout.write(
                self.style.SUCCESS("Instances of Fact successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Fact instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
