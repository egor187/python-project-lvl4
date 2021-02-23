from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    class Meta():
        ordering = ['username']

    def __str__(self):
        # return first_name and last_name of User model with space between
        return self.get_full_name()

    def get_absolute_url(self):
        return '/users/'
