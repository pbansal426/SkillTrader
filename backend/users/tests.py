from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import CustomUser

class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.change_password_url = reverse('change-password')

        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="StrongPass123"
        )

    def test_register_user(self):
        data = {
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "NewPass123",
            "password2": "NewPass123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email="new@example.com").exists())

    def test_login_user(self):
        data = {
            "email": "test@example.com",
            "password": "StrongPass123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.access_token = response.data["access"]  # Store for use in next test

    def test_change_password(self):
        self.test_login_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {
            "old_password": "StrongPass123",
            "new_password": "NewerPass456",
            "new_password2": "NewerPass456"
        }
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Password updated successfully")

