from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from clients.models import Client
from clients.serializers import ClientSerializer

class ClientApiGetAllTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123')
        self.other_user = User.objects.create_user(username='otheruser', password='Password123')
        
        self.client1 = Client.objects.create(user=self.user, first_name='John', last_name='Doe', email='john.doe@example.com', phone_number='1234567890', address='123 Street')
        self.client2 = Client.objects.create(user=self.user, first_name='Jane', last_name='Doe', email='jane.doe@example.com', phone_number='0987654321', address='456 Avenue')
        
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_list_clients_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/clients/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        expected_data = ClientSerializer([self.client1, self.client2], many=True).data
        self.assertEqual(response.data, expected_data)
    
    def test_list_clients_no_clients(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        Client.objects.filter(user=self.user).delete()
        
        response = self.client.get('/clients/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "No clients found."})
    
    def test_list_clients_unauthenticated(self):
        response = self.client.get('/clients/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_clients_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.other_user).access_token}')
        
        response = self.client.get('/clients/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "No clients found."})
