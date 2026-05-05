from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor


class Command(BaseCommand):
    help = "Keeps Supabase active and reports status to Sentry Cron Monitor."

    def handle(self, *args, **options):
        with monitor(monitor_slug="portfolio-supabase-heartbeat"):
            get_user_model().objects.exists()
            self.stdout.write(self.style.SUCCESS("Heartbeat OK"))
