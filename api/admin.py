from django.contrib import admin
from .models import Role, User, Delivery, Product, Order, OrderProduct

admin.site.register([Role, User, Delivery, Product, Order, OrderProduct])

