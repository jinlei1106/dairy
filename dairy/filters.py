from django_filters import FilterSet

from .models import Daily


class DairyFilter(FilterSet):

    class Meta:
        model = Daily
        fields = {
            'title': ('icontains',),
            'content': ('icontains',),
            'created': ('lte', 'gte'),
            'updated': ('lte', 'gte'),
        }
