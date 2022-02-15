from rest_framework import serializers

from star_wars.models import CSVFileData


class CSVFileDataSerializer(serializers.Serializer):

    class Meta:
        model = CSVFileData

    id = serializers.IntegerField(read_only=True)
    filename = serializers.CharField(source='representation_name')


class BaseParamsSerializer(serializers.Serializer):
    csv_id = serializers.IntegerField(min_value=1)


class PeopleParamsSerializer(BaseParamsSerializer):
    start_idx = serializers.IntegerField(default=0, min_value=0)
    stop_idx = serializers.IntegerField(default=10, min_value=10)


class ValueCountParamsSerializer(BaseParamsSerializer):
    name = serializers.BooleanField(required=False)
    height = serializers.BooleanField(required=False)
    mass = serializers.BooleanField(required=False)
    hair_color = serializers.BooleanField(required=False)
    skin_color = serializers.BooleanField(required=False)
    eye_color = serializers.BooleanField(required=False)
    birth_year = serializers.BooleanField(required=False)
    gender = serializers.BooleanField(required=False)
    homeworld = serializers.BooleanField(required=False)
    date = serializers.BooleanField(required=False)
