from django.db import models

# Create your models here.


class User_post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')


class Comments(models.Model):
    name =models.CharField(max_length=30)
    desc= models.TextField()
    create_at= models.DateTimeField(auto_created=True)