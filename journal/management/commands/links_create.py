from django.core.management import BaseCommand

from journal.models import Link, Platform
from utils.management.read_json import read_json_file


class Command(BaseCommand):
    help = "Create Link instances."

    def handle(self, *args, **options):
        path = "journal/management/commands/data/journal_data.json"
        data = read_json_file(json_path=path)
        link_data = data["Links"]

        for entry in link_data:
            fields = entry["fields"]
            platform_id = fields["platform"]

            try:
                platform_instance = Platform.objects.get(pk=platform_id)
            except Platform.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Platform pk={platform_id} not found, skipped.")
                )
                continue
            try:
                link, created = Link.objects.get_or_create(
                    title=fields["title"],
                    platform=platform_instance,
                    url=fields["url"],
                    defaults={
                        "active": fields["active"],
                        "panel": fields.get("panel", "JOURNAL"),
                    },
                )
                if created:
                    Link.objects.filter(pk=link.pk).update(
                        created=fields["created"],
                        updated=fields["updated"],
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Created: '{link.title} ({link.pk})'")
                    )
                else:
                    self.stdout.write(f"Skipped (exists): '{link.title} ({link.pk})'")

            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(f"Error on '{fields.get('title')}': {exc}")
                )
