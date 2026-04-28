import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from doridoro.models import Job
from utils.management.read_json import read_json_file


class Command(BaseCommand):
    help = "This command creates all Job instances for DoriDoro."

    # TODO: description modified to JSONField()

    def handle(self, *args, **options):
        path = "doridoro/management/commands/data/profile_data.json"
        data = read_json_file(json_path=path)
        job_data = data["Jobs"]

        try:
            for job in job_data:
                Job.objects.get_or_create(
                    position_en=job["position"]["en"],
                    company_name=job["company_name"],
                    start_date=job["start_date"],
                    defaults={
                        "position_de": job["position"]["de"],
                        "position_fr": job["position"]["fr"],
                        "address_en": job["address"]["en"],
                        "address_de": job["address"]["de"],
                        "address_fr": job["address"]["fr"],
                        "description_en": job["description"]["en"],
                        "description_de": job["description"]["de"],
                        "description_fr": job["description"]["fr"],
                        "end_date": job.get("end_date"),
                        "until_present": job.get("until_present", False),
                        "job_type": job["job_type"],
                    },
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Job: '{job["company_name"]}' successfully created!"
                    )
                )

        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(
                    "[IntegrityError] - These Job instances exists already!"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"[ERROR] - Job - An unexpected error occurred: {e}")
            )
