# clients/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_client, name='create-client'),
    path('', views.list_clients, name='list-clients'),
    path('<uuid:pk>/' , views.get_client_with_id, name='get-client-by-id'),
    path('update/<uuid:pk>/', views.update_client, name='update-client'),
    path('delete/<uuid:pk>/', views.delete_client, name='delete-client'),
    path('dashboard/', views.dashboard, name='search-clients'),
]
