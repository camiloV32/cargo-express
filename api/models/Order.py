from django.core.exceptions import ValidationError
from datetime import datetime
from django.db import models
from .Delivery import Delivery
from .Product import Product
class Order(models.Model):
    order_code = models.UUIDField(null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    class Meta():
        db_table = 'Order'
