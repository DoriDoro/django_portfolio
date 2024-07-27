import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Fact


class Command(BaseCommand):
    help = "This command creates all Fact instances for DoriDoro."

    def get_facts(self, path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                facts = data["Fact"]

                return facts

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"The file {path} was not found."))
        except IOError:
            self.stdout.write(
                self.style.ERROR(
                    f"An error occurred while trying to read the file {path}."
                )
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f"The file {path} does not contain valid JSON.")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
        return None

    def handle(self, *args, **options):
        path = "doridoro/management/commands/data_doridoro.json"

        facts = self.get_facts(path)
        if facts is None:
            return None

        if Fact.objects.exists():
            self.stdout.write(
                self.style.WARNING("These instances of Fact exists already!")
            )
            return

        try:
            with transaction.atomic():
                for fact in facts:
                    Fact.objects.create(
                        title_en=fact["title"]["en"],
                        title_de=fact["title"]["de"],
                        title_fr=fact["title"]["fr"],
                        content_en=fact["content"]["en"],
                        content_de=fact["content"]["de"],
                        content_fr=fact["content"]["fr"],
                    )

            self.stdout.write(
                self.style.SUCCESS("Instances of Fact successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Fact instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
