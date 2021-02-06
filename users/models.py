from django.db import models
from django.urls import reverse

class User(models.Model):
    username = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return '/users/%i/' % self.id
