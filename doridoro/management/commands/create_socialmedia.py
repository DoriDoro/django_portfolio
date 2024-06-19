from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import SocialMedia


class Command(BaseCommand):
    help = "This command creates all SocialMedia instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            social_media = [
                {
                    "name": "LinkedIn",
                    "url": "https://fr.linkedin.com/in/dorothea-reher",
                },
                {"name": "GitHub", "url": "https://github.com/DoriDoro"},
                {"name": "Dev articles", "url": "https://dev.to/doridoro"},
            ]

            if SocialMedia.objects.exists():
                self.stdout.write(
                    self.style.WARNING(
                        "These instances of Social Media exists already!"
                    )
                )
                return

            with transaction.atomic():
                for profile in social_media:
                    SocialMedia.objects.create(name=profile["name"], url=profile["url"])

            self.stdout.write(
                self.style.SUCCESS("Instances of SocialMedia successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Social Media instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
