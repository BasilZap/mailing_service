from django.contrib import admin
from blog.models import Article


@admin.register(Article)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'image', 'views', 'publication_date')

