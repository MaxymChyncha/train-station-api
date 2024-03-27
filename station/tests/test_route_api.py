from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import Route
from station.serializers.route_serializers import (
    RouteDetailSerializer,
    RouteListSerializer
)
from station.utils.samples import (
    sample_user,
    sample_superuser,
    sample_station,
    sample_route
)

ROUTE_ID = 1
ROUTE_URL = reverse("station:route-list")
ROUTE_DETAIL_URL = reverse("station:route-detail", kwargs={"pk": ROUTE_ID})


class UnauthenticatedRouteApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.route = sample_route()
        self.client.force_authenticate(self.user)

    def test_list_route(self):
        sample_route()

        res = self.client.get(ROUTE_URL)

        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("results"), serializer.data)

    def test_retrieve_route(self):
        res = self.client.get(ROUTE_DETAIL_URL)

        serializer = RouteDetailSerializer(self.route)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_route_forbidden(self):
        data = {
            "source": sample_station(),
            "destination": sample_station(name="new_station"),
            "distance": 10
        }
        res = self.client.post(ROUTE_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_routes_by_source(self):
        new_route = sample_route(source=sample_station(name="new_station"))

        res = self.client.get(ROUTE_URL, {"source": "new_sta"})

        default_route_serializer = RouteListSerializer(self.route)
        new_route_serializer = RouteListSerializer(new_route)

        self.assertIn(new_route_serializer.data, res.data.get("results"))
        self.assertNotIn(
            default_route_serializer.data,
            res.data.get("results")
        )

    def test_filter_routes_by_destination(self):
        new_route = sample_route(
            destination=sample_station(name="new_station")
        )

        res = self.client.get(ROUTE_URL, {"destination": "new_sta"})

        default_route_serializer = RouteListSerializer(self.route)
        new_route_serializer = RouteListSerializer(new_route)

        self.assertIn(new_route_serializer.data, res.data.get("results"))
        self.assertNotIn(
            default_route_serializer.data,
            res.data.get("results")
        )


class AdminRouteApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_superuser()
        self.route = sample_route()
        self.client.force_authenticate(self.user)

    def test_create_route(self):
        data = {
            "source": sample_station(name="source_station").id,
            "destination": sample_station(name="destination_station").id,
            "distance": 20
        }
        res = self.client.post(ROUTE_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_with_the_same_source_and_destination(self):
        station = sample_station()
        data = {
            "source": station.id,
            "destination": station.id,
            "distance": 20
        }
        res = self.client.post(ROUTE_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data.get("non_field_errors")[0],
            "Source can't be equal to Destination"
        )

    def test_update_route_not_allowed(self):
        data = {"distance": 20}

        res = self.client.put(ROUTE_DETAIL_URL, data)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_route_not_allowed(self):
        res = self.client.delete(ROUTE_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
