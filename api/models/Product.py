from django.db import models

class Product(models.Model):
    id = models.CharField(primary_key=True,max_length=20)
    name = models.CharField(max_length=40)
    price = models.DecimalField(decimal_places=3, max_digits=15)

    class Meta():
        db_table = 'Product'