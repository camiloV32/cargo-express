from django.urls import path
from .views import register_order, generate_token_delivery

urlpatterns = [
    path('registrar_pedido_entregado/', register_order, name='register_order'),
    path('obtener_token_delivery/', generate_token_delivery, name='generate_token_delivery')
]
