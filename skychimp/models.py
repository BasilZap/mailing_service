from django.db import models
from django.conf import settings

from skychimp.constants import CHOICE_PERIOD, STATE_CHOICE

NULLABLE = {'blank': True, 'null': True}


# Модель "Клиент"
class Client(models.Model):
    client_email = models.EmailField(verbose_name='Почтовый адрес', unique=True)
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Краткий комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Владелец')

    def __str__(self):
        return f'{self.full_name}({self.client_email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


# Модель "Письмо"
class UserMail(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тема письма')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'


# Модель "Настройка рассылки"
class MailingConfig(models.Model):

    clients = models.ManyToManyField(Client, verbose_name='Клиент')
    message = models.ForeignKey(UserMail, on_delete=models.DO_NOTHING, verbose_name='Сообщение')
    mailing_start_time = models.DateTimeField(verbose_name='Время начала рассылки', **NULLABLE)
    mailing_period = models.CharField(max_length=6, choices=CHOICE_PERIOD, default='day', verbose_name='Периодичность '
                                                                                                       'рассылки')
    mailing_stop_time = models.DateTimeField(verbose_name='Время окончания рассылки', **NULLABLE)
    mailing_state = models.CharField(max_length=1, choices=STATE_CHOICE, default='C', verbose_name='Статус')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Владелец')

    def __str__(self):
        return f'{self.mailing_start_time}, once per {self.mailing_period}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'
        permissions = (("stop_mailing", "can stop mailing"),)


# Модель "Статус рассылки"
class MailingTry(models.Model):
    mailing = models.ForeignKey(MailingConfig, on_delete=models.CASCADE, verbose_name='Рассылка')
    try_time = models.DateTimeField(verbose_name='Дата попытки')
    try_state = models.BooleanField(verbose_name='Статус попытки', **NULLABLE)
    server_response = models.CharField(max_length=200, verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        return f'{self.try_time} - {self.try_state}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
