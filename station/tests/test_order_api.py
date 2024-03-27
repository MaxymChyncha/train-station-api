from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import Order
from station.serializers.order_serializers import OrderListSerializer
from station.utils.samples import (
    sample_user,
    sample_order,
    sample_trip
)

ORDER_URL = reverse("station:order-list")


class UnauthenticatedOrderApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_list_order(self):
        sample_order(user=self.user)
        sample_order(user=self.user)

        res = self.client.get(ORDER_URL)

        orders = Order.objects.filter(user=self.user)
        serializer = OrderListSerializer(orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("results"), serializer.data)

    def test_create_order_with_tickets(self):
        data = {
            "tickets": [
                {
                    "cargo": 1,
                    "seat": 1,
                    "trip": sample_trip().id
                }
            ]
        }
        res = self.client.post(ORDER_URL, data=data, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_order_without_tickets(self):
        data = {"tickets": []}

        res = self.client.post(ORDER_URL, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data.get("tickets").get("non_field_errors")[0],
            "This list may not be empty."
        )
