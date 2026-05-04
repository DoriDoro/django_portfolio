import sentry_sdk
from sentry_sdk.crons import MonitorStatus
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Keeps Supabase active and reports status to Sentry Cron Monitor."

    def handle(self, *args, **options):
        check_in_id = sentry_sdk.capture_checkin(
            monitor_slug="portfolio-supabase-heartbeat",
            status=MonitorStatus.IN_PROGRESS,
        )
        try:
            get_user_model().objects.exists()
            sentry_sdk.capture_checkin(
                monitor_slug="portfolio-supabase-heartbeat",
                status=MonitorStatus.OK,
                check_in_id=check_in_id,
            )
            self.stdout.write(self.style.SUCCESS("Heartbeat OK"))
        except Exception as exc:
            sentry_sdk.capture_checkin(
                monitor_slug="portfolio-supabase-heartbeat",
                status=MonitorStatus.ERROR,
                check_in_id=check_in_id,
            )
            raise
