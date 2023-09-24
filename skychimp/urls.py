from skychimp.apps import SkychimpConfig
from django.urls import path
from skychimp.views import MailingListView

app_name = SkychimpConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='view'),
]
