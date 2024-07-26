import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import DoriDoro

UserModel = get_user_model()


class Command(BaseCommand):
    help = "This command creates one DoriDoro instance."

    def get_descriptions(self, path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                doridoro_descriptions = data["DoriDoro"]

                return doridoro_descriptions

        except FileNotFoundError:
            print(f"The file {path} was not found.")
        except IOError:
            print(f"An error occurred while trying to read the file {path}.")
        except json.JSONDecodeError:
            print(f"The file {path} does not contain valid JSON.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return None

    def handle(self, *args, **options):
        if (
            not DoriDoro.objects.exists()
            and not UserModel.objects.filter(username="doridoro").exists()
        ):
            path = "doridoro/management/commands/data_doridoro.json"

            descriptions = self.get_descriptions(path)
            if descriptions is None:
                return None

            try:
                with transaction.atomic():
                    user = UserModel.objects.create_user(
                        username="doridoro",
                        password="DoroPassWord147",
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
                        introduction=descriptions[0]["introduction"]["en"],
                        dream_job=descriptions[1]["dream_job"]["en"],
                        free_time=descriptions[2]["free_time"]["en"],
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
