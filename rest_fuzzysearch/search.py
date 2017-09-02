import itertools
from collections import OrderedDict

from django.db.models import Value, TextField, FloatField
from django.db.models.functions import Concat
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import filters

from .mixin import ViewSetMixin


class SearchFilter(filters.SearchFilter):

    def get_search_terms(self, request):
        params = ' '.join(request.query_params.getlist(self.search_param))
        return params.replace(',', ' ').split()


class RankedFuzzySearchFilter(SearchFilter):

    @staticmethod
    def search_queryset(queryset, search_fields, search_terms, min_rank):
        full_text_vector = sum(itertools.zip_longest(search_fields, (), fillvalue=Value(' ')), ())
        if len(search_fields) > 1:
            full_text_vector = full_text_vector[:-1]

        full_text_expr = Concat(*full_text_vector, output_field=TextField())

        similarity = TrigramSimilarity(full_text_expr, search_terms)

        queryset = queryset.annotate(rank=similarity)

        if min_rank > 0.0:
            queryset = queryset.filter(rank__gte=min_rank)

        return queryset

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)
        search_terms = ' '.join(self.get_search_terms(request))

        if search_fields and search_terms:
            min_rank = getattr(view, 'min_rank', 0.0)

            queryset = self.search_queryset(queryset, search_fields, search_terms, min_rank)

        else:
            queryset = queryset.annotate(rank=Value(1.0, output_field=FloatField()))

        return queryset


class SearchableModelMixin(ViewSetMixin):
    search_fields = ()

    min_rank = 0.0

    def list(self, request, *args, **kwargs):
        query_terms = request.query_params.getlist(SearchFilter.search_param)

        if query_terms:
            words = ' '.join(query_terms).replace(',', ' ').split()
            terms = ' '.join(words)
        else:
            terms = None

        context = OrderedDict(terms=terms)

        return self.decorated_list(SearchableModelMixin, context, request, *args, **kwargs)
