import django_filters


from .models import Patient


class PatientFilters(django_filters.FilterSet):
    age_min = django_filters.NumberFilter(field_name='age', lookup_expr='gte')
    age_max = django_filters.NumberFilter(field_name='age', lookup_expr='lte')

    examine_date_start = django_filters.DateFilter(field_name='examine_date', lookup_expr='gte')
    examine_date_end = django_filters.DateFilter(field_name='examine_date', lookup_expr='lte')

    trimester = django_filters.CharFilter(lookup_expr='exact')

    examine_by = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Patient
        fields = ['age', 'examine_date', 'trimester', 'examine_by']
