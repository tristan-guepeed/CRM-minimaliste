from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class ClientApiCreateTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123')

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_create_client_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'phone_number': '0987654321',
            'address': '456 Avenue'
        }

        response = self.client.post('/clients/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'Jane')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'jane.doe@example.com')
        self.assertEqual(response.data['phone_number'], '0987654321')
        self.assertEqual(response.data['address'], '456 Avenue')

    def test_create_client_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        invalid_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'invalidemail',
            'phone_number': '0987654321',
            'address': '456 Avenue'
        }

        response = self.client.post('/clients/create/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_client_missing_field(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        invalid_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': '0987654321',
            'address': '456 Avenue'
        }

        response = self.client.post('/clients/create/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_create_client_unauthenticated(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'phone_number': '0987654321',
            'address': '456 Avenue'
        }

        response = self.client.post('/clients/create/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
