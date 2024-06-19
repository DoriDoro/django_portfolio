from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "This command creates one DoriDoro instance and all other model instances inside "
        "the doridoro application."
    )

    def handle(self, *args, **options):
        call_command("create_superuser")
        call_command("create_doridoro")
        call_command("create_achievement")
        call_command("create_degree")
        call_command("create_fact")
        call_command("create_hobby")
        call_command("create_job")
        call_command("create_language")
        call_command("create_reference")
        call_command("create_socialmedia")
        call_command("create_website")
