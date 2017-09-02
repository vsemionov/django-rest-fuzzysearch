from django.db import migrations
from django.contrib.postgres import operations


class Migration(migrations.Migration):

    initial = True

    operations = [
        operations.TrigramExtension(),
    ]
