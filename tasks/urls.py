from django.urls import path
from tasks import views
from django_filters.views import FilterView
from tasks.filters import TaskFilter
from tasks.models import Task

app_name = 'tasks'

urlpatterns = [
    path('', views.ListTasksView.as_view(), name='tasks_list'),
    path('<int:pk>', views.TaskView.as_view(), name='task'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path(
        '<int:pk>/update/',
        views.UpdateTaskView.as_view(),
        name='update_task'
    ),
    path(
        '<int:pk>/delete/',
        views.DeleteTaskView.as_view(),
        name='delete_task'
    ),
    path('filter/', FilterView.as_view(model=TaskFilter), name='filter_task'),
    path('filter/', FilterView.as_view(model=Task), name='filter_task'),
]
