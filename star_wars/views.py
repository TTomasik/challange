import petl as etl

from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from star_wars.models import CSVFileData
from star_wars.serializers import CSVFileDataSerializer,\
    PeopleParamsSerializer, ValueCountParamsSerializer
from star_wars.utils import get_table_from_csv_id, StarWarsAPI


STAR_WARS_API_EXCEPTION = 'Problems occurred when requesting STAR WARS API.'
FILE_NOT_FOUND_EXCEPTION = 'File with provided id does not exists.'


class StarWarsView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        try:
            StarWarsAPI().fetch_and_save_data()
        except Exception:
            return Response(
                data={'detail': STAR_WARS_API_EXCEPTION},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_201_CREATED)


class CSVFileDataView(viewsets.ModelViewSet):
    queryset = CSVFileData.objects.all().order_by("-id")
    serializer_class = CSVFileDataSerializer
    http_method_names = ['get']
    permission_classes = (AllowAny,)


class PeopleView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):

        serializer = PeopleParamsSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        csv_id = serializer.data["csv_id"]
        start_idx = serializer.data["start_idx"]
        stop_idx = serializer.data["stop_idx"]

        people_table = get_table_from_csv_id(csv_id)

        try:
            if stop_idx > etl.nrows(people_table):
                stop_idx = etl.nrows(people_table)

            data = list(etl.rowslice(people_table, start_idx, stop_idx))
            return Response(
                data={"data": data, "results": len(data) - 1},
                status=status.HTTP_200_OK
            )
        except FileNotFoundError:
            return Response(
                data={'detail': FILE_NOT_FOUND_EXCEPTION},
                status=status.HTTP_400_BAD_REQUEST
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

        try:
            return Response(
                data={"data": list(etl.valuecounts(people_table, *value_to_aggregate))},
                status=status.HTTP_200_OK
            )
        except FileNotFoundError:
            return Response(
                data={'detail': FILE_NOT_FOUND_EXCEPTION},
                status=status.HTTP_400_BAD_REQUEST
            )
