from django.core.management import BaseCommand

from journal.models import Platform
from utils.management.read_json import read_json_file


class Command(BaseCommand):
    help = "Create Platform instances."

    def handle(self, *args, **options):
        path = "journal/management/commands/data/journal_data.json"
        data = read_json_file(json_path=path)
        platform_data = data["Platform"]

        for entry in platform_data:
            fields = entry["fields"]
            try:
                platform, created = Platform.objects.get_or_create(name=fields["name"])
                if created:
                    # set old created - only via bypassing save() and pre_save() with
                    # QuerySet.update()
                    Platform.objects.filter(pk=platform.pk).update(
                        created=fields["created"],
                        updated=fields["updated"],
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Platform "{platform.name} ({platform.pk})" created'
                        )
                    )
                else:
                    self.stdout.write(
                        f"Skipped (exists): '{platform.name} ({platform.pk})'"
                    )

            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(f"Error on '{fields.get('name')}': {exc}")
                )
