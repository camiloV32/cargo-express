from django.urls import path
from .views import dashboard, login

urlpatterns = [
    path('login/', login, name='login'),
    path('admin/', dashboard, name='admin'),
]
