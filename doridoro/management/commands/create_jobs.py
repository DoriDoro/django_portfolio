import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.utils.html import format_html, format_html_join

from doridoro.models import Job


class Command(BaseCommand):
    help = "This command creates all Job instances for DoriDoro."

    def get_jobs(self, path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                jobs = data["Job"]

                for job in jobs:
                    job["job_type"] = getattr(Job, job["job_type"])

                    if "until_present" in job:
                        job["until_present"] = job["until_present"].lower() == "true"

                return jobs

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"The file {path} was not found."))
        except IOError:
            self.stdout.write(
                self.style.ERROR(
                    f"An error occurred while trying to read the file {path}."
                )
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f"The file {path} does not contain valid JSON.")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
        return None

    def handle(self, *args, **options):
        path = "doridoro/management/commands/data_doridoro.json"

        jobs = self.get_jobs(path)
        if jobs is None:
            return None

        if Job.objects.exists():
            self.stdout.write(
                self.style.WARNING("These instances of Job exists already!")
            )
            return

        try:
            with transaction.atomic():
                for job in jobs:
                    formatted_description = format_html(
                        "<ul>{}</ul>",
                        format_html_join(
                            "",
                            "<li><i class='bi bi-chevron-right'></i>{}</li>",
                            ((item,) for item in job["description"]),
                        ),
                    )

                    job.pop("description")

                    Job.objects.create(description=formatted_description, **job)

            self.stdout.write(
                self.style.SUCCESS("Instances of Job successfully created!")
            )

        except IntegrityError:
            self.stdout.write(self.style.WARNING("These Job instances exists already!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
