import django_filters
from tasks.models import Task, Label

# class TaskFilter(django_filters.FilterSet):
#     new = django_filters.CharFilter(field_name='label', label='Метка')
#     class Meta:
#         model = Task
#         fields = ['task_status', 'assigned_to', 'label', 'creator', 'new']

class TaskFilter(django_filters.FilterSet):
    """By adding 'new_name' with passed 'label'-kwarg in HTML field name in filter section will change. Also for this
    purpose need to define type of filter for 'new_name' field (ModelMultipleChoiceFilter) which also need to
    pass 'queryset'-kwarg from Label model. At the end in Meta by choosing fields of a model we define 'new_name'
     field"""
    new_name = django_filters.ModelMultipleChoiceFilter(queryset=Label.objects.all(), field_name='label', label='Метка')
    class Meta:
        model = Task
        fields = ['task_status', 'assigned_to', 'creator', 'new_name']