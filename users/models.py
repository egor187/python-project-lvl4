from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    class Meta():
        ordering = ['username']

    def __str__(self):
        """String representation of user model."""
        return self.get_full_name()

    def get_absolute_url(self):
        # return f'/users/{self.id}/'
        return f'/users/'
