from django.shortcuts import redirect, render
from django.core.mail import send_mail
from users.forms import UserRegisterForm, UserForm
from django.urls import reverse_lazy, reverse
from users.models import User
from django.views.generic import CreateView, UpdateView, DeleteView, ListView


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('skychimp:list')
    template_name = 'users/register.html'


# Контроллер редактирования пользователя
class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    # def get_object(self, queryset=None):
    #     return self.request.user


class UserListView(ListView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:user_list')


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('users:user_list')
