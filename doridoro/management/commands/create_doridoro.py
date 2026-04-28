import logging

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Profile
from utils.management.read_json import read_json_file

logger = logging.getLogger(__name__)
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
                    phone_number_en=data["phone_number"]["en"],
                    phone_number_de=data["phone_number"]["de"],
                    phone_number_fr=data["phone_number"]["fr"],
                    address_en=data["address"]["en"],
                    address_de=data["address"]["de"],
                    address_fr=data["address"]["fr"],
                    profession_en=data["profession"]["en"],
                    profession_de=data["profession"]["de"],
                    profession_fr=data["profession"]["fr"],
                    introduction_en=data["introduction"]["en"],
                    introduction_de=data["introduction"]["de"],
                    introduction_fr=data["introduction"]["fr"],
                    dream_job_en=data["dream_job"]["en"],
                    dream_job_de=data["dream_job"]["de"],
                    dream_job_fr=data["dream_job"]["fr"],
                )

            except IntegrityError:
                self.stdout.write(
                    self.style.WARNING(
                        "[IntegrityError] - An instance of DoriDoro exists already!"
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"[ERROR] - An unexpected error occurred: {e}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("DoriDoro instance successfully created!")
                )
