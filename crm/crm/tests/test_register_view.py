from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class RegisterApiTests(APITestCase):

    def test_register_success(self):
        valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Password123',
        }

        response = self.client.post('/register/', valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully!')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_missing_field(self):
        invalid_data = {
            'username': 'newuser2',
            'email': 'newuser2@example.com'
        }

        response = self.client.post('/register/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_invalid_email(self):
        invalid_data = {
            'username': 'newuser3',
            'password': 'Password123',
            'email': 'invalid-email'
        }

        response = self.client.post('/register/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_short_password(self):
        invalid_data = {
            'username': 'newuser4',
            'password': 'short',
            'email': 'newuser4@example.com'
        }

        response = self.client.post('/register/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_missing_uppercase(self):
        invalid_data = {
            'username': 'newuser5',
            'password': 'password123',
            'email': 'newuser5@example.com'
        }

        response = self.client.post('/register/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_missing_digit(self):
        invalid_data = {
            'username': 'newuser6',
            'password': 'Password',
            'email': 'newuser6@example.com'
        }

        response = self.client.post('/register/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_duplicate_username(self):
        User.objects.create_user(username='existinguser', password='Password123', email='existinguser@example.com')

        invalid_data = {
            'username': 'existinguser',
            'password': 'Password123',
            'email': 'newuser7@example.com'
        }

        response = self.client.post('/register/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_blank_field(self):
        invalid_data = {
            'username': '',
            'password': 'Password123',
            'email': 'newuser8@example.com'
        }

        response = self.client.post('/register/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
