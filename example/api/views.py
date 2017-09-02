from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_fuzzysearch import search, sort

from .serializers import UserSerializer


class UserViewSet(sort.SortedModelMixin,
                  search.SearchableModelMixin,
                  viewsets.ReadOnlyModelViewSet):
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = (search.RankedFuzzySearchFilter, sort.OrderingFilter)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering_fields = ('rank', 'username', 'date_joined', 'last_login', 'first_name', 'last_name', 'email')
    ordering = ('-rank', 'date_joined',)

    min_rank = 0.25
