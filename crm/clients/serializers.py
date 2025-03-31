from rest_framework import serializers
from .models import Client

from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        
        client = Client.objects.create(user=user, **validated_data)
        return client
