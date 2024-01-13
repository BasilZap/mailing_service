from django.db import models
from skychimp.models import NULLABLE


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='blog/', verbose_name='Фото', **NULLABLE)
    views = models.IntegerField(verbose_name='Количество просмотров', default=0)
    publication_date = models.DateField(verbose_name='Дата публикации', auto_now_add=True, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
