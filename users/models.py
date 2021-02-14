from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    class Meta():
        ordering = ['username']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return f'/users/{self.id}/'
