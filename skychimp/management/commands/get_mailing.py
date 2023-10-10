from skychimp.service import send_mails
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_mails()

