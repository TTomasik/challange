from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from star_wars.models import CSVFileData


class TestStarWarsViews(APITestCase):
    def setUp(self):
        self.csv_files_url = reverse('csv-files-list')
        self.fetch_url = reverse('fetch-newest-collection-list')
        self.people_url = reverse('people-list')

    def test_get_csv_files(self):
        response = self.client.get(self.csv_files_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_newest_collection(self):
        with patch('star_wars.utils.StarWarsAPI.fetch_and_save_data'):
            response = self.client.post(self.fetch_url)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_people_without_required_params(self):
        # no required *csv_id* param
        response = self.client.get(self.people_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # - in */fetch_newest_collection* endpoint I would also test if new instance of *CSVFileData*
    #   has been created
    # - in */people* endpoint I would also test success with proper *start_idx* and *stop_idx* params
    #   to check if the data in response is complete and proper (amount of objects etc.)
    # - rest of endpoints should be tested in the same way (successes and fails as well)

