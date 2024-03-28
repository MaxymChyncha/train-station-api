from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import Station
from station.serializers.station_serializers import StationSerializer
from station.utils.samples import (
    sample_user,
    sample_superuser,
    sample_station
)

STATION_URL = reverse("station:station-list")


def detail_url(station_id):
    return reverse("station:station-detail", args=[station_id])


class UnauthenticatedStationApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(STATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTrainApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.station = sample_station()
        self.client.force_authenticate(self.user)

    def test_list_station(self):
        sample_station()

        res = self.client.get(STATION_URL)

        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("results"), serializer.data)

    def test_retrieve_station(self):
        res = self.client.get(detail_url(self.station.id))

        serializer = StationSerializer(self.station)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_train_forbidden(self):
        data = {
            "name": "test_station",
            "latitude": 4.0,
            "longitude": 5.0
        }
        res = self.client.post(STATION_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTrainApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_superuser()
        self.station = sample_station()
        self.client.force_authenticate(self.user)

    def test_create_train(self):
        data = {
            "name": "test_station",
            "latitude": 4.0,
            "longitude": 5.0
        }
        res = self.client.post(STATION_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_station_not_allowed(self):
        data = {"name": "new_station_name"}

        res = self.client.put(detail_url(self.station.id), data)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_station_not_allowed(self):
        res = self.client.delete(detail_url(self.station.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
