from django.shortcuts import redirect, render
from django.core.mail import send_mail
from users.forms import UserRegisterForm, UserForm
from django.urls import reverse_lazy, reverse
from users.models import User
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from random import randint
from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:verify_spoiler')
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()
        # Получаем данные пользователя
        user_pk = self.object.pk
        user_mail = self.object.email
        v_code = ''.join(str(randint(0, 9)) for _ in range(6))  # Генерируем проверочный код
        self.object.verify_code = v_code
        self.object.save()  # Запоминаем проверочный код и сохраняем в базе
        # send_mail(
        #     subject='Пройдите верификацию, перейдите по ссылке:',
        #     message=f'http://127.0.0.1:8000/users/register/verify?pk={user_pk}&code={v_code}',
        #     from_email=EMAIL_HOST_USER,
        #     recipient_list=[user_mail]
        # )       # Отправляем email с проверочной ссылкой пользователю
        print(f'http://127.0.0.1:8000/users/register/verify?pk={user_pk}&code={v_code}')  # Дублируем ссылку в консоль
        self.object.save()
        return super().form_valid(form)


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


def verify_email(request):
    """
    Контроллер верификации пользователя перешедшего по ссылке
    из email
    """
    # Получаем из get-запроса с формы pk и код
    user_pk = request.GET.get('pk')
    code = request.GET.get('code')
    # Проверка что pk число для предотвращения ошибки
    if user_pk.isdigit():
        # Проверка того, что код и pk пользователя совпадают с данными текущего пользователя
        if request.user.verify_code == code and request.user.pk == int(user_pk):
            request.user.is_verified = True
            request.user.save()     # Если данные совпали - устанавливаем флаг is_verified и сохраняем
            messages.success(request, 'Верификация пройдена ')
            return redirect(reverse('users:login'))
        else:
            # Если код и pk пользователя не совпадают с данными текущего пользователя - выдаем ошибку
            messages.error(request, f"Верификация не пройдена, перейдите по ссылке из email ")
    else:
        # pk не число - выдаем ошибку
        messages.error(request, f"Некорректные данные")

    return render(request, 'users/verify_email.html')


def verify_spoiler(request):
    return render(request, 'users/verify_spoiler.html')


def get_verify(request):
    """
    Контроллер запроса на верификацию. Генерирует проверочный код
    для пользователя, формирует ссылку для проверки.
    """
    # Получаем данные пользователя
    user_pk = request.user.pk
    user_mail = request.user.email
    v_code = ''.join(str(randint(0, 9)) for _ in range(6))  # Генерируем проверочный код
    request.user.verify_code = v_code
    request.user.save()     # Запоминаем проверочный код и сохраняем в базе
    # send_mail(
    #     subject='Пройдите верификацию, перейдите по ссылке:',
    #     message=f'http://127.0.0.1:8000/users/register/verify?pk={user_pk}&code={v_code}',
    #     from_email=EMAIL_HOST_USER,
    #     recipient_list=[user_mail]
    # )       # Отправляем email с проверочной ссылкой пользователю
    print(f'http://127.0.0.1:8000/users/register/verify?pk={user_pk}&code={v_code}')  # Дублируем ссылку в консоль
    return redirect(reverse('blog:random_articles'))
