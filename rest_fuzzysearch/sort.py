import itertools
from collections import OrderedDict

from rest_framework import filters, exceptions

from .mixin import ViewSetMixin


def get_sort_order(request, param):
    args = request.query_params.getlist(param)
    fields = itertools.chain(*(arg.split(',') for arg in args))
    order = tuple(field.strip() for field in fields if field)
    return order


class OrderingFilter(filters.OrderingFilter):

    @staticmethod
    def get_translated_sort_order(fields, field_map):
        return tuple(field_map.get(field, field) for field in fields)

    @staticmethod
    def get_reverse_translated_sort_order(fields, field_map):
        sort_field_reverse_map = {value: key for (key, value) in field_map.items()}
        return tuple(sort_field_reverse_map.get(field, field) for field in fields)

    @staticmethod
    def get_consistent_sort_order(fields):
        return fields + type(fields)(('pk',))

    def get_ordering(self, request, queryset, view):
        fields = get_sort_order(request, self.ordering_param)

        if fields:
            field_map = getattr(view, 'sort_field_map', {})

            fields = self.get_translated_sort_order(fields, field_map)
            ordering = self.remove_invalid_fields(queryset, fields, view, request)

            if len(ordering) != len(fields):
                ext_fields = self.get_reverse_translated_sort_order(fields, field_map)
                ext_ordering = self.get_reverse_translated_sort_order(ordering, field_map)

                errors = {}

                for ext_field in ext_fields:
                    if ext_field not in ext_ordering:
                        errors[ext_field] = 'invalid field'

                raise exceptions.ValidationError(errors)

            ordering = self.get_consistent_sort_order(ordering)

        else:
            ordering = self.get_default_ordering(view)

        consistent_sort = getattr(view, 'consistent_sort', True)
        if consistent_sort:
            ordering = self.get_consistent_sort_order(ordering)

        return ordering


class SortedModelMixin(ViewSetMixin):
    ordering = ()

    sort_field_map = {}
    consistent_sort = True

    def list(self, request, *args, **kwargs):
        sort = get_sort_order(request, OrderingFilter.ordering_param) or self.ordering

        context = OrderedDict(sort=','.join(sort))

        return self.decorated_list(SortedModelMixin, context, request, *args, **kwargs)
