import smtplib
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from skychimp.models import MailingConfig, MailingTry, Client

DATE_SHIFT = {'day': timedelta(days=1), 'week': timedelta(weeks=1), 'month': timedelta(days=30)}
# DATE_SHIFT = {'day': timedelta(seconds=30), 'week': timedelta(minutes=1), 'month': timedelta(seconds=90)}


def send_current_mailing(client: Client, mails: MailingConfig):
    """
    Рассылка конкретному клиенту, формирование лога
    :param client: Объект модели Client
    :param mails: Объект модели MailingConfig(рассылка)
    :return: None
    """
    dt_now = timezone.now()     # Получаем время попытки
    user_name = client.full_name    # Получаем Полное имя клиента
    user_mail = client.client_email     # Получаем email-адрес клиента
    message_title = mails.message.title     # Заголовок сообщения
    message = mails.message.body    # Сообщение для клиента
    # Отправка сообщения
    try:
        mailed = send_mail(
            subject=message_title,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user_mail]
        )  # Отправляем email с указанным сообщением
    except smtplib.SMTPException as mail_error:
        print(mail_error)
        create_mailing_log(mails, dt_now, False, 'Ошибка отправки')
    else:
        if mailed:
            print(f'{user_name}_{user_mail}_{message_title}_{message}')
            create_mailing_log(mails, dt_now, True, 'Успешно')
        else:
            create_mailing_log(mails, dt_now, False, 'Неопознанная ошибка')
    create_mailing_log(mails, dt_now, False, 'Ошибка отправки')
    print(f'{user_name}_{user_mail}_{message_title}_{message}')


def send_mails():
    """
    Функция обработки рассылки
    :return: None
    """
    dt_now = timezone.now()     # Получаем время попытки
    created_mailings = MailingConfig.objects.filter(mailing_state='C')  # Выбираем все созданные рассылки
    # Перебираем созданные рассылки,
    for mails in created_mailings:
        # Если наступило время старта рассылки перебираем клиентов и отправляем им сообщения
        if mails.mailing_start_time > dt_now:
            for c_client in mails.clients.all():
                send_current_mailing(c_client, mails)
                mails.mailing_state = 'R'       # Переводим рассылку в статус "Запущена"
                mails.save()

    active_mailings = MailingConfig.objects.filter(mailing_state='R')   # Выбираем все запущенные рассылки
    for mail in active_mailings:
        # Проверяем в логах время последней отправки для каждой рассылки
        mailing_tries = MailingTry.objects.filter(mailing=mail.pk)
        last_mailing = mailing_tries.order_by('-try_time').first()
        next_mailing = last_mailing.try_time + DATE_SHIFT[mail.mailing_period]
        # Если наступило время для следующего запуска рассылки перебираем клиентов и отправляем им сообщения
        if next_mailing < dt_now:
            for r_client in mail.clients.all():
                send_current_mailing(r_client, mail)
                # Если наступила дата окончания рассылки - переводим её в статус "Завершена"
                if mail.mailing_stop_time < dt_now:
                    mail.mailing_state = 'F'
                    mail.save()
            else:
                print('Жду')


def create_mailing_log(mailing: MailingConfig, mailing_datetime: datetime, try_state: bool, server_response: str):
    """
    Формирование логов
    :param mailing: Объект класса Рассылка
    :param mailing_datetime: Текущее время
    :param try_state: Статус попытки
    :param server_response: Ответ сервера
    :return: None
    """
    MailingTry.objects.create(
        mailing=mailing,
        try_time=mailing_datetime,
        try_state=try_state,
        server_response=server_response
    )


# Запуск Apscheduler
def start_scheduler():
    """Запускает крон для периодической проверки активных рассылок"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mails, trigger=CronTrigger(second='*/10'))
    scheduler.start()
