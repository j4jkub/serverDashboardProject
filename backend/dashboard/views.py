from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SystemMetricSerializer
from .models import SystemMetric
from .filters import SystemMetricFilter
from django_filters import rest_framework as django_filters
from datetime import datetime
from django.db.models import Avg
from django.db.models.functions import TruncMinute

class DashboardView(viewsets.ModelViewSet):
    serializer_class = SystemMetricSerializer
    filterset_class = SystemMetricFilter
    filter_backends = (django_filters.DjangoFilterBackend,)
    queryset = SystemMetric.objects.all().order_by('-timestamp')
    pagination_class = None