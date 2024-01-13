from skychimp.apps import SkychimpConfig
from django.urls import path
from skychimp.views import MailingListView, MailingCreateView, ClientCreateView, UserMailCreateView, MailingDeleteView,\
    MailingTryListView, MailingUpdateView, ManagerMailingUpdateView

app_name = SkychimpConfig.name

urlpatterns = [
    path('create/', MailingCreateView.as_view(), name='create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),
    path('mailing_try/', MailingTryListView.as_view(), name='mailing_try_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('create_user_mail/', UserMailCreateView.as_view(), name='create_user_mail'),
    path('manage_mails/<int:pk>/', ManagerMailingUpdateView.as_view(), name='manage_mails'),
    path('', MailingListView.as_view(), name='list'),
]
