from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Модель "Клиент"
class Client(models.Model):
    client_email = models.EmailField(verbose_name='Почтовый адрес', unique=True)
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Краткий комментарий')

    def __str__(self):
        return f'{self.full_name}'

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
    STATE_CHOICE = [
        ('F', 'завершена'),
        ('R', 'запущена'),
        ('C', 'создана'),
    ]

    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, verbose_name='Клиент')
    message = models.ForeignKey(UserMail, on_delete=models.DO_NOTHING, verbose_name='Сообщение')
    mailing_time = models.TimeField(verbose_name='Время рассылки', **NULLABLE)
    mailing_period = models.DurationField(verbose_name='Периодичность рассылки')
    mailing_state = models.CharField(max_length=1, choices=STATE_CHOICE, default='C', verbose_name='Статус')

    def __str__(self):
        return f'{self.mailing_time} - {self.mailing_period}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'


# Модель "Статус рассылки"
class MailingTry(models.Model):
    mailing = models.ForeignKey(MailingConfig, on_delete=models.CASCADE, verbose_name='Рассылка')
    try_time = models.DateTimeField(verbose_name='Дата попытки')
    try_state = models.BooleanField(verbose_name='Статус попытки', **NULLABLE)
    server_response = models.CharField(max_length=200, verbose_name='Ответ сервера', **NULLABLE)

    def __str__(self):
        if self.try_state is not None:
            if self.try_state:
                state_str = 'Успешно'
            else:
                state_str = 'Ошибка'
        else:
            state_str = 'Не определено'
        return f'{self.try_time} - статус: {state_str}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

