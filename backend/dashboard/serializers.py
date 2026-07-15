from rest_framework import serializers
from .models import SystemMetric

class SystemMetricSerializer(serializers.ModelSerializer):
    # timestamp = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        fields = '__all__'
        model = SystemMetric