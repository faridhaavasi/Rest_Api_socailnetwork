from django.db import models
from apps.users.models import User
# Create your models here.



class AccountModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500,null=True ,blank=True)

    def __str__(self):
        return self.user.username
    
    
