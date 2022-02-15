from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from star_wars.models import CSVFileData


class TestStarWarsViews(APITestCase):
    def setUp(self):
        self.csv_files_url = reverse('csv-files')
        self.fetch_url = reverse('fetch-newest-collection')
        self.people_url = reverse('people')

    def test_get_csv_files(self):
        response = self.client.get(self.csv_files_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_newest_collection(self):
        nmb_of_files_before = CSVFileData.objects.count()
        response = self.client.get(self.fetch_url)
        nmb_of_files_after = CSVFileData.objects.count()
        assert response.status_code == status.HTTP_201_CREATED
        assert nmb_of_files_before + 1 == nmb_of_files_after

    def test_get_people_without_required_params(self):
        # no required *csv_id* param
        response = self.client.get(self.people_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # - in */people* endpoint I would test also success with proper *start_idx* and *stop_idx* params
    #   to check if the data in response is complete and proper (amount of objects etc.)
    # - rest of endpoints should be tested in the same way (successes and fails as well)

