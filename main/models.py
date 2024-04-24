from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    role = models.CharField(max_length=50, default="Regular User")
    def __str__(self):
        return self.user.username
    
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    audit_date = models.DateField()
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name