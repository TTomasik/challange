import datetime
import petl as etl
import requests

from django.shortcuts import get_object_or_404

from star_wars.models import CSVFileData
from star_wars.constants import INITIAL_PLANETS_URL, INITIAL_PEOPLE_URL,\
    CSV_REGULAR_COLUMNS, CSV_CUSTOM_COLUMNS, CSV_FILES_DIR_PATH


class StarWarsAPI:
    def __init__(self):
        self.all_people = []
        self.all_planets = {}
        self.initial_urls = [INITIAL_PLANETS_URL, INITIAL_PEOPLE_URL]

    def set_data(self, *, obj, url):
        if url.startswith(INITIAL_PLANETS_URL):
            self.all_planets[obj['url']] = obj['name']
        else:
            data = []
            for column in CSV_REGULAR_COLUMNS:
                data.append(obj[column])
            data.extend([
                self.all_planets[obj['homeworld']],
                datetime.date.today().strftime('%Y-%m-%d')
            ])
            self.all_people.append(data)

    def fetch_data(self, *, url):
        response = requests.get(url)
        if response.ok:
            response_data = response.json()
            for obj in response_data.get('results', []):
                self.set_data(obj=obj, url=url)
            next_page = response_data.get('next')
            if next_page:
                return self.fetch_data(url=next_page)

    def save_data(self):
        filename = datetime.datetime.now().strftime('%h-%d-%Y-%I-%M-%p')
        # create CSVFileData's instance
        csv_file_data = CSVFileData.objects.create(filename=filename)
        # create CSV file
        etl.tocsv(
            [CSV_REGULAR_COLUMNS + CSV_CUSTOM_COLUMNS] + self.all_people,
            f'{CSV_FILES_DIR_PATH}{filename}_{csv_file_data.id}.csv'
        )

    def fetch_and_save_data(self):
        for url in self.initial_urls:
            self.fetch_data(url=url)
        return self.save_data()


def get_table_from_csv_id(csv_id):
    csv_file_data = get_object_or_404(CSVFileData, id=csv_id)
    filename = csv_file_data.csv_name
    return etl.fromcsv(f'{CSV_FILES_DIR_PATH}{filename}')
