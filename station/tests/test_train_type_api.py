from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import TrainType
from station.serializers.train_type_serializers import TrainTypeSerializer
from station.utils.samples import (
    sample_user,
    sample_superuser,
    sample_train_type
)

TRAIN_TYPE_URL = reverse("station:train-type-list")


class UnauthenticatedTrainTypeApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TRAIN_TYPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTrainTypeApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_list_train_type(self):
        sample_train_type()
        sample_train_type()

        res = self.client.get(TRAIN_TYPE_URL)

        train_types = TrainType.objects.all()
        serializer = TrainTypeSerializer(train_types, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("results"), serializer.data)

    def test_create_train_type_forbidden(self):
        data = {"name": "test_train_type"}
        res = self.client.post(TRAIN_TYPE_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTrainTypeApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_superuser()
        self.client.force_authenticate(self.user)

    def test_create_train_type(self):
        data = {"name": "test_train_type"}
        res = self.client.post(TRAIN_TYPE_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrainType.objects.last().name, "test_train_type")
