import django_filters
from tasks.models import Task, Label

# class TaskFilter(django_filters.FilterSet):
#     new = django_filters.CharFilter(field_name='label', label='Метка')
#     class Meta:
#         model = Task
#         fields = ['task_status', 'assigned_to', 'label', 'creator', 'new']

class TaskFilter(django_filters.FilterSet):
    new_name = django_filters.ModelMultipleChoiceFilter(queryset=Label.objects.all(), field_name='label', label='Метка')
    class Meta:
        model = Task
        fields = ['task_status', 'assigned_to', 'creator', 'new_name']