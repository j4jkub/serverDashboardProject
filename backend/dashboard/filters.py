import django_filters
from .models import SystemMetric

class SystemMetricFilter(django_filters.FilterSet):
    timestamp = django_filters.DateTimeFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(
            attrs={"type": "datetime-local"}
        ))
    last = django_filters.NumberFilter(method="filter_last", label="Last N Records")

    class Meta:
        model = SystemMetric
        fields = {
            'timestamp',
        }
    
    def filter_last(self, queryset, name, value):
        ids = (
            queryset.order_by("-timestamp")[:value]
            .values_list("id", flat=True)
        )

        return queryset.filter(id__in=ids).order_by("timestamp")