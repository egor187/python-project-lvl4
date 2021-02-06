from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views

app_name='users'

urlpatterns = [
#    path('', include('django.contrib.auth.urls')),
    path('', views.ListUserView.as_view(), name='user_list'),
    path('<int:pk>/', views.UserView.as_view(template_name='user_view.html'), name='user'),
    path('create/', views.CreateUserView.as_view(template_name='user_create_form.html'), name='create_user'),
    path('<int:pk>/delete/>', views.DeleteUserView.as_view(template_name='user_delete.html'), name='delete_user'),
    path('<int:pk>/update/', views.UpdateUserView.as_view(template_name='user_update.html'), name='update_user'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html')),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
]
