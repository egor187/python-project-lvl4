from django.db import models
from users.models import CustomUser


class TaskStatus(models.Model):
    name = models.CharField('Имя', max_length=70, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/statuses/{self.id}/'

    class Meta():
        ordering = ['name']


class Label(models.Model):
    name = models.CharField('Имя', max_length=70, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/labels/{self.id}/'

    class Meta():
        ordering = ['name']


class Task(models.Model):
    name = models.CharField('Имя', max_length=50, null=True, blank=True)
    description = models.TextField(
        'Описание',
        max_length=150,
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        TaskStatus,
        verbose_name='Статус',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    creator = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='creator'
    )
    executor = models.ForeignKey(
        CustomUser,
        verbose_name='Исполнитель',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='executor'
    )
    labels = models.ManyToManyField(
        Label,
        through='RelatedModel',
        through_fields=('task', 'label'),
        blank=True,
        verbose_name='Метки'
    )

    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/tasks/{self.id}/'


class RelatedModel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
