from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:register")
TOKEN_URL = reverse("user:token_obtain_pair")
ME_URL = reverse("user:manage")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        data = {
            "email": "user@user.com",
            "password": "1234test",
            "first_name": "user_first_name",
            "last_name": "user_last_name"
        }

        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(data.get("password")))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        data = {
            "email": "user@user.com",
            "password": "1234test",
        }
        create_user(**data)

        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        data = {
            "email": "user@user.com",
            "password": "qwe",
        }
        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = (
            get_user_model().objects.filter(email=data.get("email")).exists()
        )

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        data = {
            "email": "user@user.com",
            "password": "1234test",
        }
        create_user(**data)

        res = self.client.post(TOKEN_URL, data)
        self.assertIn("refresh", res.data)
        self.assertIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(email="user@user.com", password="1234test")
        data = {
            "email": "user@user.com",
            "password": "wrong_password",
        }

        res = self.client.post(TOKEN_URL, data)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_no_user(self):
        data = {
            "email": "user@user.com",
            "password": "1234test",
        }
        res = self.client.post(TOKEN_URL, data)
        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_missing_field(self):
        data = {"email": "test", "password": ""}
        res = self.client.post(TOKEN_URL, data=data)
        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):

    def setUp(self) -> None:
        self.user = create_user(
            email="user@user.com",
            password="1234test",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "id": self.user.id,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name
            },
        )

    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, data={})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_self(self):
        data = {"email": "new@user.com", "password": "12345new"}

        res = self.client.patch(ME_URL, data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, data.get("email"))
        self.assertTrue(self.user.check_password(data.get("password")))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
