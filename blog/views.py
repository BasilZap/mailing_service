from django.shortcuts import render
from blog.models import Article
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy


class BlogListView(ListView):
    model = Article
    success_url = reverse_lazy('blog:list')


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        """
        Счетчик просмотров каждой статьи
        """
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


def random_articles(request):
    context = {'articles': Article.objects.all().order_by('?')[:3]}
    return render(request, 'blog/random_articles.html', context)
