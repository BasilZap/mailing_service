from django.apps import AppConfig


class SkychimpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skychimp'

    def ready(self):
        """Запуск Apsceduler"""
        from skychimp.service import start_scheduler
        print('started')
        start_scheduler()
