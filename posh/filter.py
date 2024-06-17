# filters.py
import django_filters
from .models import IndividualUser, NGOUser, ConsultancyUser
from django.db.models import Q

class IndividualUserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_name')
    state = django_filters.CharFilter(field_name='state', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    user_type = django_filters.CharFilter(method='filter_user_type')

    class Meta:
        model = IndividualUser
        fields = ['fname', 'state', 'city', 'type']

    def filter_by_name(self, queryset, name, value):
        # Split the input value into parts by spaces
        name_parts = value.split()

        if not name_parts:
            return queryset

        # Create a query that will match any of the given name parts in any combination
        queries = Q(fname__icontains=name_parts[0])
        if len(name_parts) > 1:
            queries |= Q(mname__icontains=name_parts[1])
        if len(name_parts) > 2:
            queries |= Q(lname__icontains=name_parts[2])

        if len(name_parts) == 1:
            # Search for single name part in any of the fields
            queries |= Q(mname__icontains=name_parts[0]) | Q(lname__icontains=name_parts[0])
        elif len(name_parts) == 2:
            # Search for combinations of two name parts
            queries |= (Q(fname__icontains=name_parts[0]) & Q(mname__icontains=name_parts[1])) | \
                       (Q(mname__icontains=name_parts[0]) & Q(lname__icontains=name_parts[1])) | \
                       (Q(fname__icontains=name_parts[0]) & Q(lname__icontains=name_parts[1]))
        elif len(name_parts) == 3:
            # Search for combinations of three name parts
            queries |= (Q(fname__icontains=name_parts[0]) & Q(mname__icontains=name_parts[1]) & Q(lname__icontains=name_parts[2])) | \
                       (Q(fname__icontains=name_parts[0]) & Q(lname__icontains=name_parts[1]) & Q(mname__icontains=name_parts[2])) | \
                       (Q(mname__icontains=name_parts[0]) & Q(fname__icontains=name_parts[1]) & Q(lname__icontains=name_parts[2])) | \
                       (Q(mname__icontains=name_parts[0]) & Q(lname__icontains=name_parts[1]) & Q(fname__icontains=name_parts[2])) | \
                       (Q(lname__icontains=name_parts[0]) & Q(fname__icontains=name_parts[1]) & Q(mname__icontains=[name_parts[2]])) | \
                       (Q(lname__icontains=[name_parts[0]]) & Q(mname__icontains=[name_parts[1]]) & Q(fname__icontains=[name_parts[2]]))

        return queryset.filter(queries)

    def filter_user_type(self, queryset, name, value):
        if value == 'Individual':
            return queryset
        return queryset.none()

class NGOUserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='ngo_name', lookup_expr='icontains')
    state = django_filters.CharFilter(field_name='ngo_state', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='ngo_city', lookup_expr='icontains')
    user_type = django_filters.CharFilter(method='filter_user_type')

    class Meta:
        model = NGOUser
        fields = ['name', 'state', 'city']

    def filter_user_type(self, queryset, name, value):
        if value == 'NGO':
            return queryset
        return queryset.none()

class ConsultancyUserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='consultancy_name', lookup_expr='icontains')
    state = django_filters.CharFilter(field_name='consultancy_state', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='consultancy_city', lookup_expr='icontains')
    user_type = django_filters.CharFilter(method='filter_user_type')

    class Meta:
        model = ConsultancyUser
        fields = ['name', 'state', 'city']

    def filter_user_type(self, queryset, name, value):
        if value == 'Consultancy':
            return queryset
        return queryset.none()
