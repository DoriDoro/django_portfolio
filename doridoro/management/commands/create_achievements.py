from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from doridoro.models import Achievement
from utils.management.read_json import read_json_file

UserModel = get_user_model()


class Command(BaseCommand):
    help = "This command creates all Achievement instances for DoriDoro."

    def handle(self, *args, **options):
        path = "doridoro/management/commands/data/profile_data.json"
        data = read_json_file(json_path=path)
        achievement_data = data["Achievements"]

        try:
            for achievement in achievement_data:
                Achievement.objects.create(
                    title_en=achievement["title"]["en"],
                    title_de=achievement["title"]["de"],
                    title_fr=achievement["title"]["fr"],
                    content_en=achievement["content"]["en"],
                    content_de=achievement["content"]["de"],
                    content_fr=achievement["content"]["fr"],
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Achievement: '{achievement["title"]["en"]} successfully created!"
                    )
                )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    "[IntegrityError] - These Achievement instances exists already!"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"[ERROR] - An unexpected error occurred: {e}")
            )
