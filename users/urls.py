from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import RegisterView, UserUpdateView, UserListView, UserDeleteView, verify_email, verify_spoiler, \
    ManageUserUpdateView
from users.apps import UsersConfig


app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('<int:pk>/user_delete/', UserDeleteView.as_view(), name='user_delete'),
    path('verify/', verify_email, name='verify_email'),
    path('verify_spoiler', verify_spoiler, name='verify_spoiler'),
    path('manage_users/<int:pk>', ManageUserUpdateView.as_view(), name='manage_users'),

    ]
