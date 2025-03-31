from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from clients.models import Client

class ClientApiUpdateTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123')
        self.other_user = User.objects.create_user(username='otheruser', password='Password123')
        
        self.client1 = Client.objects.create(user=self.user, first_name='John', last_name='Doe', email='john.doe@example.com', phone_number='1234567890', address='123 Street')
        
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_update_client_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        updated_data = {"first_name": "Johnny", "address": "789 Boulevard"}
        response = self.client.put(f'/clients/update/{self.client1.id}/', updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client1.refresh_from_db()
        self.assertEqual(self.client1.first_name, "Johnny")
        self.assertEqual(self.client1.address, "789 Boulevard")
    
    def test_update_client_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        updated_data = {"first_name": "Johnny"}
        response = self.client.put('/clients/update/999/', updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_client_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        invalid_data = {"email": "invalidemail"}
        response = self.client.put(f'/clients/update/{self.client1.id}/', invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
    
    def test_update_client_unauthenticated(self):
        updated_data = {"first_name": "Johnny"}
        response = self.client.put(f'/clients/update/{self.client1.id}/', updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_client_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.other_user).access_token}')
        updated_data = {"first_name": "Johnny"}
        response = self.client.put(f'/clients/update/{self.client1.id}/', updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)