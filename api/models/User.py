from django.contrib.auth.hashers import make_password
from django.db import models
from .Role import Role
class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    class Meta():
        db_table = 'User'

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
