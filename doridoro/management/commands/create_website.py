from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Website


class Command(BaseCommand):
    help = "This command creates all Websites instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            websites = [
                {
                    "name": "static Portfolio Flask",
                    "url": "https://portfolio-dorothea-reher.vercel.app/",
                },
                {
                    "name": "Orange Country Lettings",
                    "url": "https://oc-lettings-site-latest-c1cc.onrender.com",
                },
            ]

            if Website.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Website exists already!")
                )
                return

            with transaction.atomic():
                for website in websites:
                    Website.objects.create(name=website["name"], url=website["url"])

            self.stdout.write(
                self.style.SUCCESS("Instances of Website successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Website instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
