Django REST Fuzzy Search
========================

Fuzzy Search for Django REST Framework
--------------------------------------

[![Build Status](https://travis-ci.org/vsemionov/django-rest-fuzzysearch.svg?branch=master)](https://travis-ci.org/vsemionov/django-rest-fuzzysearch)


### Fuzzy Search

This package provides REST APIs with support for fuzzy (approximate) full-text searching. This allows searching for results with unknown exact contents, as well as searches with spelling mistakes. The returned results are ranked and may be ordered by similarity.

This package requires *PostgreSQL* and uses its trigram extension (*pg_trgm*). It provides a queryset filter and optional support viewset mixins.


### Requirements

* Python 3 (tested with 3.6)
* PostgreSQL (tested with 9.6)
* Django (>=1.11, tested with 1.11)
* Django REST Framework (tested with 3.6)


### Basic Usage

1. Install the package:
```
pip install django-rest-fuzzysearch
```

2. Add a database migration to enable the trigram extension:
```
from django.db import migrations
from django.contrib.postgres import operations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        operations.TrigramExtension(),
    ]
```
Note that running this migration would require superuser privileges of your database user. To avoid that, you could instead enable the extension manually:
```
psql -U postgres -c "create extension pg_trgm;" <database>
```

3. Add the fuzzy search filter to your viewset's filter backends:
```
    filter_backends = (search.RankedFuzzySearchFilter,)
```

4. Configure the viewset's list of model fields that will be included in the search:
```
    search_fields = ('username', 'first_name', 'last_name', 'email')
```

5. Configure a minimum rank, after which the results will be truncated (optional, default is no truncation):
```
    min_rank = 0.25
```
The rank of results varies between 0 and 1.

#### Performance

Fuzzy searching is a relatively expensive operation. If you expect it to be applied to very large sets of records, it would be beneficial to create a functional index, which matches your search fields. See the [PostgreSQL documentation][fts-index-docs] for details.

[fts-index-docs]: https://www.postgresql.org/docs/current/static/textsearch-tables.html#TEXTSEARCH-TABLES-INDEX "Creating Indexes"


### Ordering Results by Similarity

Fuzzy search is most useful when the results are ordered by similarity. To achieve this, you can use REST Framework's ordering filter and configure it the following way:
1. Enable ordering by rank by adding the latter to the list of allowed fields:
```
    ordering_fields = ('rank', ...)
```

2. Configure the default ordering in the viewset:
```
    ordering = ('-rank', ...)
```
If a search is not being performed (no terms were specified), all results will have a rank of 1. Therefore, ordering by rank is still possible, but does nothing.


### Support Classes

#### Decorating Search Results

To decorate the results with the used search terms, you can optionally inherit your viewset from *SearchableModelMixin*:
```
from rest_fuzzysearch import search
class UserViewSet(search.SearchableModelMixin,
                  ...
                  viewsets.ModelViewSet):
```
The terms will be returned in the "terms" field of the response body.

#### Advanced Ordering of Results

This package also includes a custom ordering filter and mixin to provide the following features:
* translation of ordering fields between the query parameter names and model field names
  - this is intended to be used when the internal and exposed names of your model's fields are different
* optional consistent ordering - the model's primary key (which is unique) is appended to the "order by" clause for consistency of results with otherwise equal ordering fields
* reject requests with invalid ordering fields with an http status 400
* decoration of the results with the used ordering; the ordering is returned in the "sort" field of the response body

Usage:
1. Add the custom ordering filter to your viewset's filter backends:
```
from rest_fuzzysearch import sort

...

    filter_backends = (..., sort.OrderingFilter)
```

2. Inherit your viewset from *SortedModelMixin*:
```
class UserViewSet(sort.SortedModelMixin,
                  ...
                  viewsets.ModelViewSet):
```

3. Configure the mixin with the following viewset attributes:
```
    sort_field_map = {'id': 'ext_id'}  # field translation map; keys are external field names, values are internal field names; default is no translation
    consistent_sort = True             # whether the primary key should be appended to the ordering for consistency; default is True
```


### Example Project

For a working example project that integrates this package, see the */example* directory. To run it:
```
cd example
pip install -r requirements.txt
# configure the database connection in example/settings.py
python manage.py migrate
python manage.py runserver
```
