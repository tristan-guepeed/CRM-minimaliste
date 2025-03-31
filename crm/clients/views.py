from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_client(request):
    if request.method == 'POST':
        serializer = ClientSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_clients(request):
    if request.method == 'GET':
        clients = Client.objects.filter(user=request.user)
        if not clients.exists():
            return Response({"message": "No clients found."}, status=status.HTTP_200_OK)
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_client_with_id(request, pk):
    try:
        client = Client.objects.get(pk=pk, user=request.user)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_client(request, pk):
    try:
        client = Client.objects.get(pk=pk, user=request.user)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_client(request, pk):
    try:
        client = Client.objects.get(pk=pk, user=request.user)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def dashboard(request):
    total_clients = Client.objects.count()

    recent_clients = Client.objects.filter(created_at__gte="2025-01-01")

    search_query = request.GET.get('search', '')
    if search_query:
        clients = Client.objects.filter(
            first_name__icontains=search_query) | Client.objects.filter(last_name__icontains=search_query) | Client.objects.filter(email__icontains=search_query)
    else:
        clients = Client.objects.all()

    recent_count = recent_clients.count()

    context = {
        'total_clients': total_clients,
        'recent_count': recent_count,
        'clients': clients,
        'search_query': search_query,
    }
    return render(request, 'dashboard.html', context)
