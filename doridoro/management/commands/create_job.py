from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from doridoro.models import Job


class Command(BaseCommand):
    help = "This command creates all Job instances for DoriDoro."

    def handle(self, *args, **options):
        try:
            jobs = [
                {
                    "name": "Cocoonr Hosting Power and Book&Pay",
                    "title": "Apprenticeship as Python Developer",
                    "start_date": "2022-11-24",
                    "until_present": True,
                    "description": """I have effectively utilized Notion as an integral tool for 
                    managing project workflows. My expertise includes working on tasks within 
                    Notion, where I have seamlessly created, tracked, and completed independently 
                    various project assignments, ensuring timely delivery and adherence to 
                    project goals. Proficient in handling database requests and exporting data 
                    into CSV files. Responsible for managing the internal Slack chat 
                    "Assistance Technique," where colleagues report bugs, problems, and server 
                    errors. Skilled in checking Sentry for errors and identifying issues promptly. 
                    Experienced in verifying bugs, resolving them, or creating development 
                    requests as necessary. Capable of analyzing code to provide explanations for 
                    issues and propose solutions. Enhanced understanding of website operations 
                    and management through problem-solving activities. Proficient in generating 
                    scripts with templates for inserting new data, such as new cities, into the 
                    database. Skilled in implementing new dashboard modules and assembling custom 
                    code modules to create innovative dashboard features.
                    """,
                    "job_type": Job.APPRENTICESHIP,
                },
            ]

            if Job.objects.exists():
                self.stdout.write(
                    self.style.WARNING("These instances of Job exists already!")
                )
                return

            with transaction.atomic():
                for job in jobs:
                    Job.objects.create(
                        **job,
                    )

            self.stdout.write(
                self.style.SUCCESS("Instances of Job successfully created!")
            )

        except IntegrityError:
            self.stdout.write(self.style.WARNING("These Job instances exists already!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
