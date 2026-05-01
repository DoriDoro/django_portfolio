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
            for entry in achievement_data:
                achievement, created = Achievement.objects.get_or_create(
                    title_en=entry["title"]["en"],
                    defaults={
                        "title_de": entry["title"]["de"],
                        "title_fr": entry["title"]["fr"],
                        "content_en": entry["content"]["en"],
                        "content_de": entry["content"]["de"],
                        "content_fr": entry["content"]["fr"],
                    },
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Achievement: '{achievement.title} ({achievement.pk})' "
                            "successfully created!"
                        )
                    )

                else:
                    self.stdout.write(
                        f"Skipped (exists): '{achievement.title} ({achievement.pk})'"
                    )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"[ERROR] - An unexpected error occurred: {e}")
            )
