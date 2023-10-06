from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogListView, ArticleDetailView, random_articles


app_name = BlogConfig.name

urlpatterns = [
    path('skychimp/', random_articles, name='random_articles'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('view/<int:pk>/', ArticleDetailView.as_view(), name='view'),
]
