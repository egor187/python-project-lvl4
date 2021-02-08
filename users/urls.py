from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views import generic
from users.models import CustomUser
from users import views

app_name='users'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('', views.ListUserView.as_view(), name='user_list'),
    path('<int:pk>/', views.UserView.as_view(template_name='user_view.html'), name='user'),
    path('create/', views.CreateUserView.as_view(template_name='user_create_form.html'), name='create_user'),
    path('<int:pk>/delete/>', views.DeleteUserView.as_view(template_name='user_delete.html'), name='delete_user'),
    path('login/', views.LoginUserView.as_view(template_name='login.html'), name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),


    path('login/<int:pk>/', views.ProfileView.as_view(template_name='profile.html'), name='profile'),
    # path('login/<int:pk>/', generic.DetailView.as_view(template_name='profile.html', model=CustomUser), name='profile'),


    path('logout/', auth_views.LogoutView.as_view(template_name='login.html')),
    path('<int:pk>/update/', views.UpdateUserView.as_view(template_name='user_update.html'), name='update_user'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
]
