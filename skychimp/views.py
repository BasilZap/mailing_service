from django.shortcuts import render
from django.views.generic import ListView
from skychimp.models import MailingConfig
from skychimp.forms import MailingConfigForm
from django.urls import reverse, reverse_lazy


class MailingListView(ListView):
    model = MailingConfig
    form_class = MailingConfigForm
    success_url = reverse_lazy('skychimp:list')

