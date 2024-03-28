from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import Train
from station.serializers.train_serializers import TrainSerializer
from station.utils.samples import (
    sample_user,
    sample_superuser,
    sample_train,
    sample_train_type
)

TRAIN_URL = reverse("station:train-list")


def detail_url(train_id):
    return reverse("station:train-detail", args=[train_id])


class UnauthenticatedTrainApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TRAIN_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTrainApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.train = sample_train()
        self.client.force_authenticate(self.user)

    def test_list_train(self):
        sample_train()

        res = self.client.get(TRAIN_URL)

        trains = Train.objects.all()
        serializer = TrainSerializer(trains, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("results"), serializer.data)

    def test_retrieve_train(self):
        res = self.client.get(detail_url(self.train.id))

        serializer = TrainSerializer(self.train)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_train_forbidden(self):
        data = {
            "name": "test_train",
            "cargo_num": 10,
            "places_in_cargo": 20,
            "train_type": sample_train_type().id
        }
        res = self.client.post(TRAIN_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_train_forbidden(self):
        data = {"name": "new_train"}
        res = self.client.patch(detail_url(self.train.id), data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTrainApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_superuser()
        self.train = sample_train()
        self.client.force_authenticate(self.user)

    def test_create_train(self):
        data = {
            "name": "test_train",
            "cargo_num": 10,
            "places_in_cargo": 20,
            "train_type": sample_train_type().id
        }
        res = self.client.post(TRAIN_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_train(self):
        data = {"name": "new_train"}
        res = self.client.patch(detail_url(self.train.id), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_train_not_allowed(self):
        res = self.client.delete(detail_url(self.train.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
