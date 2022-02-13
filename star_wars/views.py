import datetime
import petl as etl
import requests

from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from star_wars.models import CSVFileData
from star_wars.serializers import CSVFileDataSerializer, PeopleParamsSerializer, ValueCountParamsSerializer


CSV_REGULAR_COLUMNS = [
    'name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender'
]
CSV_CUSTOM_COLUMNS = ['homeworld', 'date']
CSV_FILES_DIR_PATH = '/var/www/server/csv_files/'


class StarWarsAPI:
    # *swapi.co* is not supported and maintained anymore
    # this is why I used: *swapi.dev*
    INITIAL_PLANETS_URL = 'https://swapi.dev/api/planets/'
    INITIAL_PEOPLE_URL = 'https://swapi.dev/api/people/'

    def __init__(self):
        self.all_people = []
        self.all_planets = {}
        self.initial_urls = [self.INITIAL_PLANETS_URL, self.INITIAL_PEOPLE_URL]

    def set_data(self, *, obj, url):
        if url.startswith(self.INITIAL_PLANETS_URL):
            self.all_planets[obj['url']] = obj['name']
        else:
            data = []
            for key in CSV_REGULAR_COLUMNS:
                data.append(obj[key])
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


class CSVFileDataView(viewsets.ModelViewSet):
    queryset = CSVFileData.objects.all()
    serializer_class = CSVFileDataSerializer
    http_method_names = ['get']


class PeopleView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):

        serializer = PeopleParamsSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        csv_id = serializer.data["csv_id"]
        results_per_page = serializer.data["results_per_page"]

        people_table = get_table_from_csv_id(csv_id)

        if results_per_page > etl.nrows(people_table):
            results_per_page = etl.nrows(people_table)

        return Response(
            data={
                "results": results_per_page,
                "data": list(etl.head(people_table, results_per_page))
            },
            status=status.HTTP_200_OK
        )


class ValueCountView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):

        serializer = ValueCountParamsSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        request_params = serializer.data.copy()
        csv_id = request_params.pop("csv_id")

        people_table = get_table_from_csv_id(csv_id)

        value_to_aggregate = list(
            filter(lambda value: request_params[value], request_params.keys())
        )

        return Response(
            data=list(etl.valuecounts(people_table, *value_to_aggregate)),
            status=status.HTTP_200_OK
        )
