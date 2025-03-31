from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from clients.models import Client

class ClientApiDeleteTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123')
        self.other_user = User.objects.create_user(username='otheruser', password='Password123')
        
        self.client1 = Client.objects.create(user=self.user, first_name='John', last_name='Doe', email='john.doe@example.com', phone_number='1234567890', address='123 Street')
        
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_delete_client_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(f'/clients/delete/{self.client1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=self.client1.id).exists())
    
    def test_delete_client_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete('/clients/delete/999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_client_unauthenticated(self):
        response = self.client.delete(f'/clients/delete/{self.client1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_client_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.other_user).access_token}')
        response = self.client.delete(f'/clients/delete/{self.client1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Client.objects.filter(id=self.client1.id).exists())