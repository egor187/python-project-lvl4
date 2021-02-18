import django_filters
from tasks.models import Task

class TaskFilter(django_filters.FilterSet):

    class Meta:
        model = Task
        fields = ['task_status', 'assigned_to', 'label', 'creator']
