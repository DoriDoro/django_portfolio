import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import DoriDoro

UserModel = get_user_model()


class Command(BaseCommand):
    help = "This command creates one DoriDoro instance."

    # for later...
    # client = models.ForeignKey()
    # review = models.ForeignKey()

    def handle(self, *args, **options):
        if (
            not DoriDoro.objects.exists()
            and not UserModel.objects.filter(username="doridoro").exists()
        ):
            try:
                raw_password = input("Please enter the password for DoriDoro: ")

                def get_descriptions(key):
                    with open(
                        "doridoro/management/commands/descriptions.json", "r"
                    ) as file:
                        descriptions = json.load(file)
                        return descriptions.get(key)

                with transaction.atomic():
                    user = UserModel.objects.create_user(
                        username="doridoro",
                        password=raw_password,
                        email="dorothea.reher@gmail.com",
                        first_name="Dorothea",
                        last_name="Reher",
                        is_staff=True,
                    )
                    DoriDoro.objects.create(
                        user=user,
                        phone="0033768132147",
                        address="35710 Bruz in France",
                        profession="Python/Django Developer",
                        introduction=get_descriptions("profile_description"),
                        dream_job=get_descriptions("dream_job_description"),
                        free_time=get_descriptions("free_time_description"),
                    )

            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING("An instance of DoriDoro exists already!")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"An unexpected error occurred: {e}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("DoriDoro instance successfully created!")
                )
        else:
            self.stdout.write(self.style.WARNING("A DoriDoro instance exists already!"))
