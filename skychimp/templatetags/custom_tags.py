from django import template
from skychimp.models import MailingConfig, Client



register = template.Library()


# Вывод количества клиентов для рассылок
@register.simple_tag()
def total_users():
    return Client.objects.count()


# Вывод количества рассылок
@register.simple_tag()
def total_mailings():
    return MailingConfig.objects.count()


# Вывод активных рассылок
@register.simple_tag()
def active_mailings():
    count = 0
    for x in MailingConfig.objects.all():
        if x.mailing_state == 'R':
            count += 1
    return count



