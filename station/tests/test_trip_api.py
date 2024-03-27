import datetime

from django.db.models import F, Count
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import Trip
from station.serializers.trip_serializers import (
    TripDetailSerializer,
    TripListSerializer
)
from station.utils.samples import (
    sample_user,
    sample_superuser,
    sample_trip,
    sample_route,
    sample_train,
    sample_crew,
    sample_station
)

TRIP_ID = 1
TRIP_URL = reverse("station:trip-list")
TRIP_DETAIL_URL = reverse("station:trip-detail", kwargs={"pk": TRIP_ID})


class UnauthenticatedTripApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TRIP_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTripApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

        self.trip = sample_trip()
        self.another_trip = sample_trip(
            route=sample_route(
                source=sample_station(
                    name="new_source_station"
                ),
                destination=sample_station(
                    name="new_destination_station"
                )
            ),
            departure_time=datetime.datetime(year=2024, month=5, day=1),
            arrival_time=datetime.datetime(year=2024, month=5, day=2)
        )
        self.trips = Trip.objects.annotate(
            tickets_available=(
                F("train__cargo_num")
                * F("train__places_in_cargo")
                - Count("tickets")
            )
        )

    def test_list_trip(self):
        sample_trip()

        res = self.client.get(TRIP_URL)

        serializer = TripListSerializer(self.trips, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("results"), serializer.data)

    def test_retrieve_trip(self):
        res = self.client.get(TRIP_DETAIL_URL)

        serializer = TripDetailSerializer(self.trip)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_trip_forbidden(self):
        data = {
            "route": sample_route().id,
            "train": sample_train().id,
            "crew": [sample_crew().id],
            "departure_time": (
                datetime.datetime.now() + datetime.timedelta(days=1)
            ),
            "arrival_time": (
                datetime.datetime.now() + datetime.timedelta(days=2)
            ),
        }
        res = self.client.post(TRIP_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_trip_forbidden(self):
        data = {
            "arrival_time": (
                datetime.datetime.now() + datetime.timedelta(days=2)
            )
        }
        res = self.client.patch(TRIP_DETAIL_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_trip_forbidden(self):
        res = self.client.delete(TRIP_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_trips_by_source_station(self):
        res = self.client.get(TRIP_URL, {"from": "new_sour"})

        default_trip_serializer = TripListSerializer(self.trip)
        new_trip_serializer = TripListSerializer(
            self.trips.get(id=self.another_trip.id)
        )

        self.assertNotIn(default_trip_serializer.data, res.data.get("results"))
        self.assertIn(new_trip_serializer.data, res.data.get("results"))

    def test_filter_trips_by_destination(self):
        res = self.client.get(TRIP_URL, {"to": "new_destin"})

        default_trip_serializer = TripListSerializer(self.trip)
        new_trip_serializer = TripListSerializer(
            self.trips.get(id=self.another_trip.id)
        )

        self.assertNotIn(default_trip_serializer.data, res.data.get("results"))
        self.assertIn(new_trip_serializer.data, res.data.get("results"))

    def test_filter_by_departure_date(self):
        res = self.client.get(TRIP_URL, {"departure_date": "2024-05-01"})

        default_trip_serializer = TripListSerializer(self.trip)
        new_trip_serializer = TripListSerializer(
            self.trips.get(id=self.another_trip.id)
        )

        self.assertNotIn(default_trip_serializer.data, res.data.get("results"))
        self.assertIn(new_trip_serializer.data, res.data.get("results"))

    def test_filter_by_arrival_date(self):
        res = self.client.get(TRIP_URL, {"arrival_date": "2024-05-02"})

        default_trip_serializer = TripListSerializer(self.trip)
        new_trip_serializer = TripListSerializer(
            self.trips.get(id=self.another_trip.id)
        )

        self.assertNotIn(default_trip_serializer.data, res.data.get("results"))
        self.assertIn(new_trip_serializer.data, res.data.get("results"))


class AdminTripApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_superuser()
        self.trip = sample_trip()
        self.client.force_authenticate(self.user)

    def test_create_trip(self):
        data = {
            "route": sample_route().id,
            "train": sample_train().id,
            "crew": [sample_crew().id],
            "departure_time": (
                datetime.datetime.now() + datetime.timedelta(days=4)
            ),
            "arrival_time": (
                datetime.datetime.now() + datetime.timedelta(days=5)
            ),
        }
        res = self.client.post(TRIP_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_trip_with_arrival_less_than_departure_date(self):
        data = {
            "route": sample_route().id,
            "train": sample_train().id,
            "crew": [sample_crew().id],
            "departure_time": (
                datetime.datetime.now() + datetime.timedelta(days=4)
            ),
            "arrival_time": (
                datetime.datetime.now() + datetime.timedelta(days=2)
            ),
        }
        res = self.client.post(TRIP_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data.get("non_field_errors")[0],
            "Departure time can't be bigger than arrival time"
        )

    def test_update_trip(self):
        data = {
            "departure_time": (
                datetime.datetime.now() + datetime.timedelta(days=3)
            ),
            "arrival_time": (
                datetime.datetime.now() + datetime.timedelta(days=6)
            )
        }

        res = self.client.patch(TRIP_DETAIL_URL, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_trip(self):
        res = self.client.delete(TRIP_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
