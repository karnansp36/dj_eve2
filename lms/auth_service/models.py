from django.db import models

# Create your models here.
class user_jwtservices(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
 
#auth with jwt
