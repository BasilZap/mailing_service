from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from skychimp.models import MailingConfig, Client, UserMail, MailingTry
from skychimp.forms import MailingConfigForm, ClientForm, UserMailForm, MailingTryConfigForm
from django.urls import reverse, reverse_lazy


class MailingListView(ListView):
    model = MailingConfig
    form_class = MailingConfigForm
    success_url = reverse_lazy('skychimp:list')


class MailingDeleteView(DeleteView):
    model = MailingConfig
    success_url = reverse_lazy('skychimp:list')


class MailingCreateView(CreateView):
    model = MailingConfig
    form_class = MailingConfigForm
    success_url = reverse_lazy('skychimp:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        print(self.object.owner)
        return super().form_valid(form)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('skychimp:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class UserMailCreateView(CreateView):
    model = UserMail
    form_class = UserMailForm
    success_url = reverse_lazy('skychimp:list')


class MailingTryListView(ListView):
    model = MailingTry
    form_class = MailingTryConfigForm
    success_url = reverse_lazy('skychimp:list')
