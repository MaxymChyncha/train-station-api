from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from station.models import Crew
from station.serializers.crew_serializers import CrewSerializer
from station.utils.samples import (
    sample_user,
    sample_crew,
    sample_superuser
)

CREW_URL = reverse("station:crew-list")


class UnauthenticatedCrewApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_list_crew(self):
        sample_crew()
        sample_crew(first_name="John", last_name="Doe")

        res = self.client.get(CREW_URL)

        crews = Crew.objects.all()
        serializer = CrewSerializer(crews, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("results"), serializer.data)

    def test_create_crew_forbidden(self):
        data = {
            "first_name": "crew_first_name",
            "last_name": "crew_last_name",
            "position": "other",
        }
        res = self.client.post(CREW_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_superuser()
        self.client.force_authenticate(self.user)

    def test_create_crew(self):
        data = {
            "first_name": "crew_first_name",
            "last_name": "crew_last_name",
            "position": "other",
        }
        res = self.client.post(CREW_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        crew = Crew.objects.get(id=res.data.get("id"))
        for key in data.keys():
            self.assertEqual(data.get(key), getattr(crew, key))
