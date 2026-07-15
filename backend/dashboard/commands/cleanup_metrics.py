from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import SystemMetric


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        deleted, _ = SystemMetric.objects.filter(
            timestamp__lt=timezone.now() - timedelta(days=30)
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(f"Deleted {deleted} records.")
        )