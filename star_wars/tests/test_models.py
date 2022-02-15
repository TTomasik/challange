import pytest

from star_wars.models import CSVFileData
from star_wars.tests.factories import CSVFileDataFactory


@pytest.mark.django_db
class TestCSVFileData:
    def test_create_csv_file_data_instance(self):
        CSVFileDataFactory(filename='test_name')
        csv_file_data = CSVFileData.objects.first()
        assert csv_file_data.filename == 'test_name'
