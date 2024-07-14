from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "This command creates one Admin and one DoriDoro instance and all other model instances "
        "of doridoro and project application."
    )

    def handle(self, *args, **options):
        call_command("create_superuser")
        call_command("create_doridoro")
        call_command("create_achievements")
        call_command("create_degrees")
        call_command("create_facts")
        call_command("create_hobbies")
        call_command("create_jobs")
        call_command("create_languages")
        call_command("create_references")
        call_command("create_socialmedia")
        call_command("create_tags")
        call_command("create_links")
