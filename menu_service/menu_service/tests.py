from rest_framework import status
from rest_framework.test import APITestCase


REGISTER_URL = '/register/'


class RegisterUserTestCase(APITestCase):

    def test_register_valid_user(self):

        data = {
            "username": "testusername",
            "password": "testpassword"
        }

        response = self.client.post(REGISTER_URL, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_invalid_user(self):

        data = {
            "username": "testusername",
        }

        response = self.client.post(REGISTER_URL, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_register_existing_user(self):

        data = {
            "username": "testusername",
            "password": "testpassword"
        }
        self.client.post(REGISTER_URL, data, format="json")

        response = self.client.post(REGISTER_URL, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
