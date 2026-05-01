from django.core.management.base import BaseCommand
from journal.models import Journal, Link
from utils.management.read_json import read_json_file


class Command(BaseCommand):
    help = "Creates Journal instances from journal_data.json"

    def handle(self, *args, **options):
        path = "journal/management/commands/data/journal_data.json"
        data = read_json_file(json_path=path)
        journal_data = data["Journals"]

        for entry in journal_data:
            fields = entry["fields"]
            try:
                journal, created = Journal.objects.get_or_create(
                    name=fields["name"],
                    defaults={
                        "status": fields.get("status", "DF"),
                        "content": fields["content"],
                        "category": fields["category"],
                        "published": fields.get("published"),
                    },
                )
                if created:
                    Journal.objects.filter(pk=journal.pk).update(
                        created=fields["created"],
                        updated=fields["updated"],
                    )
                    for pk in fields.get("links", []):
                        try:
                            journal.links.add(Link.objects.get(pk=pk))
                        except Link.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(f"  Link pk={pk} not found, skipped")
                            )
                    self.stdout.write(
                        self.style.SUCCESS(f"Created: '{journal.name} ({journal.pk})'")
                    )
                else:
                    self.stdout.write(
                        f"Skipped (exists): '{journal.name} ({journal.pk})'"
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error on '{fields.get('name')}': {e}")
                )
