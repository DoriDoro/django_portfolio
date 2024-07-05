from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from projects.models import Link


class Command(BaseCommand):
    help = "This command creates all Job instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            links = [
                {
                    "title": "ToDoro",
                    "origin": Link.GITHUB,
                    "platform": Link.PERSONAL_PROJECT,
                    "url": "https://github.com/DoriDoro/ToDoro",
                },
                {
                    "title": "Book to Scrape",
                    "legend": "Project 2 of OpenClassrooms Python Path",
                    "origin": Link.GITHUB,
                    "platform": Link.OPENCLASSROOMS,
                    "url": "https://github.com/DoriDoro/Book_to_Scrape",
                },
                {
                    "title": "Chess Tournament",
                    "legend": "Project 4 of OpenClassrooms Python Path",
                    "origin": Link.GITHUB,
                    "platform": Link.OPENCLASSROOMS,
                    "url": "https://github.com/DoriDoro/Chess_Tournament",
                },
                {
                    "title": "Just Stream It",
                    "legend": "Project 6 of OpenClassrooms Python Path",
                    "origin": Link.GITHUB,
                    "platform": Link.OPENCLASSROOMS,
                    "url": "https://github.com/DoriDoro/JustStreamIt",
                },
                {
                    "title": "Algo Invest Trade",
                    "legend": "Project 7 of OpenClassrooms Python Path",
                    "origin": Link.GITHUB,
                    "platform": Link.OPENCLASSROOMS,
                    "url": "https://github.com/DoriDoro/algoInvest_trade",
                },
                {
                    "title": "Litrature Reviue Project",
                    "legend": "Project 9 of OpenClassrooms Python Path",
                    "origin": Link.GITHUB,
                    "platform": Link.OPENCLASSROOMS,
                    "url": "https://github.com/DoriDoro/LITRevu-project",
                },
                {
                    "title": "SoftDesk API",
                    "legend": "Project 10 of OpenClassrooms Python Path",
                    "origin": Link.GITHUB,
                    "platform": Link.OPENCLASSROOMS,
                    "url": "https://github.com/DoriDoro/SoftDesk_api",
                },
                {
                    "title": "Gudlft",
                    "legend": "Project 11 of OpenClassrooms Python Path",
                    "origin": Link.GITHUB,
                    "platform": Link.OPENCLASSROOMS,
                    "url": "https://github.com/DoriDoro/Gudlft",
                },
                {
                    "title": "Epic Events",
                    "legend": "Project 12 of OpenClassrooms Python Path",
                    "origin": Link.GITHUB,
                    "platform": Link.OPENCLASSROOMS,
                    "url": "https://github.com/DoriDoro/EpicEvents",
                },
                {
                    "title": "Orange Country Lettings",
                    "legend": "Project 13 of OpenClassrooms Python Path",
                    "origin": Link.GITHUB,
                    "platform": Link.OPENCLASSROOMS,
                    "url": "https://github.com/DoriDoro/OC_lettings",
                },
                {
                    "title": "Django Portfolio",
                    "legend": "ToDoro",
                    "origin": Link.GITHUB,
                    "platform": Link.PERSONAL_PROJECT,
                    "url": "https://github.com/DoriDoro/django_portfolio",
                },
            ]

            if Link.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Link exists already!")
                )
                return

            with transaction.atomic():
                for link in links:
                    Link.objects.create(**link)

            self.stdout.write(
                self.style.SUCCESS("Instances of Link successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Link instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
