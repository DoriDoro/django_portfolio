from django.core.management.base import BaseCommand

from doridoro.models import Job
from utils.management.read_json import read_json_file


class Command(BaseCommand):
    help = "This command creates all Job instances for DoriDoro."

    def handle(self, *args, **options):
        path = "doridoro/management/commands/data/profile_data.json"
        data = read_json_file(json_path=path)
        job_data = data["Jobs"]

        for entry in job_data:
            try:
                job, created = Job.objects.get_or_create(
                    company_name=entry.get("company_name") or "",
                    position_en=entry["position"]["en"],
                    start_date=entry["start_date"],
                    end_date=entry.get("end_date"),
                    until_present=entry.get("until_present", False),
                    job_type=entry["job_type"],
                    defaults={
                        "position_de": entry["position"]["de"],
                        "position_fr": entry["position"]["fr"],
                        "address_en": entry["address"]["en"],
                        "address_de": entry["address"]["de"],
                        "address_fr": entry["address"]["fr"],
                        "description_en": entry["description"]["en"],
                        "description_de": entry["description"]["de"],
                        "description_fr": entry["description"]["fr"],
                        "work_type": entry["work_type"],
                    },
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Created: '{job.company_name} ({job.pk})'")
                    )
                else:
                    self.stdout.write(
                        f"Skipped (exists): '{job.company_name} ({job.pk})'"
                    )
            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(
                        f"[ERROR] - Job - An unexpected error occurred: {exc}"
                    )
                )
