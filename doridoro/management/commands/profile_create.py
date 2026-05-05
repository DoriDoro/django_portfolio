from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Profile
from utils.management.read_json import read_json_file

UserModel = get_user_model()


class Command(BaseCommand):
    help = "This command creates a Profile instance."

    def handle(self, *args, **options):
        path = "doridoro/management/commands/data/profile_data.json"
        data = read_json_file(json_path=path)
        profile_data = data["Profile"]

        try:
            user = UserModel.objects.get(username="Doro")
        except UserModel.DoesNotExist:
            user = call_command(
                "createsuperuser",
                username="Doro",
                email="dorothea.reher@gmail.com",
            )

        for data in profile_data:
            try:
                Profile.objects.create(
                    user=user,
                    address_en=data["address"]["en"],
                    address_de=data["address"]["de"],
                    address_fr=data["address"]["fr"],
                    profession_en=data["profession"]["en"],
                    profession_de=data["profession"]["de"],
                    profession_fr=data["profession"]["fr"],
                    motto_en=data["motto"]["en"],
                    motto_de=data["motto"]["de"],
                    motto_fr=data["motto"]["fr"],
                    introduction_en=data["introduction"]["en"],
                    introduction_de=data["introduction"]["de"],
                    introduction_fr=data["introduction"]["fr"],
                    more_details_en=data["more_details"]["en"],
                    more_details_de=data["more_details"]["de"],
                    more_details_fr=data["more_details"]["fr"],
                )

            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING(
                        "[IntegrityError] - An instance of DoriDoro exists already!"
                    )
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[ERROR] - An unexpected error occurred: {e}"))
            else:
                self.stdout.write(self.style.SUCCESS("DoriDoro instance successfully created!"))
