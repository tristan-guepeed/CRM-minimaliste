from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class LoginApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123', email='testuser@example.com')

    def test_login_success(self):
        valid_data = {
            'username': 'testuser',
            'password': 'Password123',
        }

        response = self.client.post('/login/', valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_login_invalid_credentials(self):
        invalid_data = {
            'username': 'testuser',
            'password': 'WrongPassword',
        }

        response = self.client.post('/login/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], "Username or password is incorrect.")


    def test_login_missing_fields(self):
        missing_username = {
            'password': 'Password123',
        }

        response = self.client.post('/login/', missing_username, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'][0], "This field is required.")


        missing_password = {
            'username': 'testuser',
        }

        response = self.client.post('/login/', missing_password, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], "This field is required.")

    def test_login_blank_fields(self):
        blank_data = {
            'username': '',
            'password': '',
        }

        response = self.client.post('/login/', blank_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('username', response.data)
        self.assertIn('password', response.data)

        self.assertEqual(response.data['username'][0], "This field may not be blank.")
        self.assertEqual(response.data['password'][0], "This field may not be blank.")


    def test_login_invalid_username(self):
        invalid_data = {
            'username': 'nonexistentuser',
            'password': 'Password123',
        }

        response = self.client.post('/login/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], "Username or password is incorrect.")

    def test_login_incorrect_password(self):
        invalid_data = {
            'username': 'testuser',
            'password': 'IncorrectPassword',
        }

        response = self.client.post('/login/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], "Username or password is incorrect.")

