from django.urls import path
from .consumers import monitoringApp

websocket_urlpatterns = [
    path('ws/monitoring/', monitoringApp.as_asgi()),
]