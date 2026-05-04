import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "This command creates one Super User, one Profile instance and all achievements,"
        "degrees, jobs, languages, social media, links and skills."
    )

    def handle(self, *args, **options):
        call_command("createsuperuser", username="Doro", email="dorothea.reher@gmail.com")
        self.stdout.write(" -- Start creating Profile --")
        call_command("profile_create")
        self.stdout.write(" -- Starting Profile details --")
        self.stdout.write(" -- Achievements --")
        call_command("achievements_create")
        self.stdout.write(" -- Degrees --")
        call_command("degrees_create")
        self.stdout.write(" -- Jobs --")
        call_command("jobs_create")
        self.stdout.write(" -- Languages --")
        call_command("languages_create")
        self.stdout.write(" -- Social Media --")
        call_command("social_media_create")
        self.stdout.write(" -- Starting Journal details --")
        self.stdout.write(" -- Platform --")
        call_command("platform_create")
        self.stdout.write(" -- Links --")
        call_command("links_create")
        self.stdout.write(" -- Journals --")
        call_command("journals_create")
        self.stdout.write(" -- Starting Project details --")
        self.stdout.write(" -- Skills --")
        call_command("skills_create")
        self.stdout.write(" -- Projects --")
        call_command("projects_create")
