from django.db import models

class Users(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

# Create your models here.
