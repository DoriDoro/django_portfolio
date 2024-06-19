from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Achievement

UserModel = get_user_model()


class Command(BaseCommand):
    help = "This command creates all Achievement instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            achievements = [
                {
                    "title": "Formation",
                    "content": (
                        "In July 2024: Completed a 24-month training program in just 20 months."
                    ),
                },
                {
                    "title": "Relocate",
                    "content": (
                        "Relocated to Rennes and started a formation within 6 weeks, despite the "
                        "challenge of finding accommodation."
                    ),
                },
                {
                    "title": "Single parent",
                    "content": (
                        "Single parent, working full-time (80% in enterprise and 20% formation)."
                    ),
                },
                {
                    "title": "French",
                    "content": (
                        "Undertook formation in French, despite limited proficiency in the "
                        "language."
                    ),
                },
                {
                    "title": "Challenges",
                    "content": (
                        "Demonstrated resilience and adaptability in overcoming challenges."
                    ),
                },
                {
                    "title": "Self",
                    "content": (
                        "Proved commitment to continuous self-improvement and ability to thrive "
                        "in adverse situations."
                    ),
                },
                {
                    "title": "Myself",
                    "content": (
                        "Through sheer determination and perseverance, I navigated through the "
                        "complexities of the coursework and emerged victorious, showcasing my "
                        "resilience and adaptability in adverse situations."
                    ),
                },
            ]

            if Achievement.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Achievement exists already!")
                )
                return

            with transaction.atomic():
                for achievement in achievements:
                    Achievement.objects.create(
                        title=achievement["title"], content=achievement["content"]
                    )

            self.stdout.write(
                self.style.SUCCESS("Instances of Achievement successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Achievement instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
