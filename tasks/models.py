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


class Label(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=70, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/labels/{self.id}/'

    class Meta():
        ordering = ['name']


class Task(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True,)
    description = models.CharField(max_length=150, null=True, blank=True,)
    task_status = models.ForeignKey(TaskStatus, null=True, blank=True, on_delete=models.PROTECT)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='creator')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned')
    label = models.ManyToManyField(Label)

    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/tasks/{self.id}/'