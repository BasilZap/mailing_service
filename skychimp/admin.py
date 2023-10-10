from django.contrib import admin
from skychimp.models import MailingConfig, UserMail, MailingTry, Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_email', 'full_name', 'comment', 'owner')


@admin.register(UserMail)
class UserMailAdmin(admin.ModelAdmin):
    list_display = ('title', 'body',)


@admin.register(MailingConfig)
class MailingConfigAdmin(admin.ModelAdmin):
    list_display = ('message', 'mailing_start_time', 'mailing_period', 'mailing_stop_time', 'mailing_state')

# 'client',


@admin.register(MailingTry)
class MailingTryAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'try_time', 'try_state', 'server_response')

