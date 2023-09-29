from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import RegisterView, UserUpdateView, UserListView, UserDeleteView
from users.apps import UsersConfig


app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('<int:pk>/user_delete/', UserDeleteView.as_view(), name='user_delete'),
    ]
