import datetime
import factory.fuzzy

from star_wars.models import CSVFileData


class CSVFileDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CSVFileData

    date = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(2022, 2, 2, tzinfo=datetime.timezone.utc)
    )
    filename = factory.Sequence(lambda n: f'csv_file_data_{n}')
