from django.urls import path
from django.views import generic
from tasks import views

app_name = 'tasks'

urlpatterns = [
    path('statuses/', views.ListStatusesView.as_view(), name='statuses_list'),
    path('statuses/<int:pk>/', views.StatusView.as_view(template_name='status_view.html'), name='status'),
    path('statuses/<int:pk>/update/', views.UpdateStatusView.as_view(), name='update_status'),
    path('statuses/<int:pk>/delete/', views.DeleteStatusView.as_view(), name='delete_status'),
    path('statuses/create/', views.CreateStatusView.as_view(), name='create_status'),

]
