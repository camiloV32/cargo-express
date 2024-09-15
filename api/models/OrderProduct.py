from django.db import models
from .Order import Order
from .Product import Product
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  

    class Meta():
        db_table = 'OrderProduct'