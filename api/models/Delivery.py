from django.db import models
from .User import User
class Delivery(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta():
        db_table = 'Delivery'
