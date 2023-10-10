from django.shortcuts import render
from blog.models import Article
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy


# Контроллер вывода списка статей
class BlogListView(ListView):
    model = Article
    success_url = reverse_lazy('blog:list')


# Контроллер просмотра статьи
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


# Контроллер вывода 3х рандомных статей списка статей
def random_articles(request):
    context = {'articles': Article.objects.all().order_by('?')[:3]}
    return render(request, 'blog/random_articles.html', context)
