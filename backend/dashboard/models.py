from django.db import models
from datetime import datetime

# Create your models here.
class SystemMetric(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    cpu_usage_avg = models.FloatField()
    cpu_usage_min = models.FloatField()
    cpu_usage_max = models.FloatField()

    ram_usage_avg = models.FloatField()
    ram_usage_min = models.FloatField()
    ram_usage_max = models.FloatField()

    disk_used = models.BigIntegerField()

    def __str__(self):
        return f"{self.timestamp}"