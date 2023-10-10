from users.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@adminov.ru',
            first_name='admin',
            last_name='Superuser',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('123456')
        user.save()
