import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Achievement

UserModel = get_user_model()


class Command(BaseCommand):
    help = "This command creates all Achievement instances for DoriDoro."

    def get_achievements(self, path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                achievements = data["Achievement"]

                return achievements

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

        achievements = self.get_achievements(path)
        if achievements is None:
            return None

        if Achievement.objects.exists():
            self.stdout.write(
                self.style.WARNING("These instances of Achievement exists already!")
            )
            return

        try:
            with transaction.atomic():
                for achievement in achievements:
                    Achievement.objects.create(**achievement)

            self.stdout.write(
                self.style.SUCCESS("Instances of Achievement successfully created!")
            )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING("These Achievement instances exists already!")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
