"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from task_manager import views

app_name = 'task_manager'

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('login/', views.LoginUserView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutUserView.as_view(template_name='login.html'), name='logout'),
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),

    path('labels/', views.ListLabelsView.as_view(), name='labels_list'),
    path('labels/<int:pk>/', views.LabelView.as_view(), name='label'),
    path('labels/create/', views.CreateLabelView.as_view(), name='create_label'),
    path('labels/<int:pk>/update/', views.UpdateLabelView.as_view(), name='update_label'),
    path('labels/<int:pk>/delete/', views.DeleteLabelView.as_view(), name='delete_label'),

    path('admin/', admin.site.urls),
]
