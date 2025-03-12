from django.db import models

# Create your models here.
class TokenModel(models.Model):
    token = models.CharField()
    value = models.CharField()



        
