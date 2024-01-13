from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, ArticleDetailView, random_articles


app_name = BlogConfig.name

urlpatterns = [
    path('skychimp/', cache_page(60)(random_articles), name='random_articles'),
    path('blog_list/', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('view/<int:pk>/', ArticleDetailView.as_view(), name='view'),
]
