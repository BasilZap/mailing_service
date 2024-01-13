from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from skychimp.models import MailingConfig, Client, UserMail, MailingTry
from skychimp.forms import MailingConfigForm, ClientForm, UserMailForm, MailingTryConfigForm, \
    ModeratorMailingConfigForm
from django.urls import reverse, reverse_lazy

from users.models import User


# Контроллер формы отображения всех рассылок пользователя
class MailingListView(LoginRequiredMixin, ListView):
    model = MailingConfig
    form_class = MailingConfigForm
    success_url = reverse_lazy('skychimp:list')

    # Фильтруем для вывода заявки созданные текущим пользователем
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


# Контроллер удаления рассылки
class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingConfig
    success_url = reverse_lazy('skychimp:list')


# Контроллер формы создания рассылки
class MailingCreateView(LoginRequiredMixin, CreateView):
    model = MailingConfig
    form_class = MailingConfigForm
    success_url = reverse_lazy('skychimp:list')

    # Выборка клиентов, которых создал текущий пользователь
    def get_form_kwargs(self) -> dict[str, User]:

        kwargs = super(MailingCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Если данные верны, добавляем текущего пользователя как создателя
    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


# Контроллер формы изменения рассылки
class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingConfig
    form_class = MailingConfigForm
    success_url = reverse_lazy('skychimp:list')

    # Выборка клиентов, которых создал текущий пользователь
    def get_form_kwargs(self) -> dict[str, User]:

        kwargs = super(MailingUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Если данные верны, добавляем текущего пользователя как создателя
    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


# Форма создания клиента
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('skychimp:list')

    # Если данные верны, добавляем текущего пользователя как создателя
    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


# Форма создания сообщения
class UserMailCreateView(LoginRequiredMixin, CreateView):
    model = UserMail
    form_class = UserMailForm
    success_url = reverse_lazy('skychimp:list')


# Форма просмотра логов
class MailingTryListView(ListView):
    model = MailingTry
    form_class = MailingTryConfigForm
    success_url = reverse_lazy('skychimp:list')


# Форма отключения рассылок для менеджера
class ManagerMailingUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingConfig
    form_class = ModeratorMailingConfigForm
    success_url = reverse_lazy('skychimp:list')


