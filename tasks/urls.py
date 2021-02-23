from django.urls import path
from django.views import generic
from tasks import views
from django_filters.views import FilterView
from tasks.filters import TaskFilter
from tasks.models import Task

app_name = 'tasks'

urlpatterns = [
    # path('statuses/', views.ListStatusesView.as_view(), name='statuses_list'),
    # path('statuses/<int:pk>/', views.StatusView.as_view(template_name='status_view.html'), name='status'),
    # path('statuses/create/', views.CreateStatusView.as_view(), name='create_status'),
    # path('statuses/<int:pk>/update/', views.UpdateStatusView.as_view(), name='update_status'),
    # path('statuses/<int:pk>/delete/', views.DeleteStatusView.as_view(), name='delete_status'),

    path('', views.ListTasksView.as_view(), name='tasks_list'),
    path('<int:pk>', views.TaskView.as_view(), name='task'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/update/', views.UpdateTaskView.as_view(), name='update_task'),
    path('<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete_task'),
    path('filter/', FilterView.as_view(model=TaskFilter), name='filter_task'),
    path('filter/', FilterView.as_view(model=Task), name='filter_task'),

    # path('labels/', views.ListLabelsView.as_view(), name='labels_list'),
    # path('labels/<int:pk>/', views.LabelView.as_view(), name='label'),
    # path('labels/create/', views.CreateLabelView.as_view(), name='create_label'),
    # path('labels/<int:pk>/update/', views.UpdateLabelView.as_view(), name='update_label'),
    # path('labels/<int:pk>/delete/', views.DeleteLabelView.as_view(), name='delete_label'),
]
