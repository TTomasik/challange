from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestStarWarsViews(APITestCase):
    def setUp(self):
        self.csv_files_url = reverse('csv-files')

    def test_get_csv_files(self):
        response = self.client.get(self.csv_files_url)
        assert response.status_code == status.HTTP_200_OK

    # - rest of endpoints could be tested in the same way
    # - different HTTP statuses should be tested as well
