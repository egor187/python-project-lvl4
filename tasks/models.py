from django.db import models
from users.models import CustomUser


class TaskStatus(models.Model):
    name = models.CharField(max_length=70, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/statuses/{self.id}/'

    class Meta():
        ordering = ['name']


class Labels(models.Model):
    name = models.CharField(max_length=70, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/labels/{self.id}/'

    class Meta():
        ordering = ['name']


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    task_status = models.ForeignKey(TaskStatus, on_delete=models.PROTECT)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='creator')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='assigned')
    label = models.ManyToManyField(Labels)

    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/tasks/{self.id}/'