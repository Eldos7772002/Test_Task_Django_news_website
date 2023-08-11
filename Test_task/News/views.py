from django.http import request, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import Category, Author, Article, Country
from django.db.models import Prefetch
import requests
import pymorphy2



class CategoryListView(ListView):
    model = Category
    category_name = "Шоу-биз"  # Замените на нужное имя категории
    category = Category.objects.get(name=category_name)
    template_name = 'News/category_list.html'  # Создайте этот шаблон

def Count(requests):
    countries = Country.objects.all()
    articles_by_category = {}

    for idx, country in enumerate(countries):
        countries[idx].dative_name = add_dative_ending_russian(country.name)  # Добавляем поле с именем в дательном падеже
        context = {

            'articles_by_category': articles_by_category,
            'countries': countries,

        }
    return render(request, 'news/base.html', context)


def show_category(request, category_name):
    try:
        category = Category.objects.get(name=category_name)
        articles = Article.objects.filter(category=category)
    except Category.DoesNotExist:
        category = None
        articles = []

    latest_article = articles.first()
    other_articles = articles[1:]

    if latest_article:
        latest_article.views += 1  # Увеличиваем счетчик просмотров
        latest_article.save()
    context = {
        'category': category,
        'latest_article': latest_article,
        'other_articles': other_articles,
        'articles': articles,
    }

    return render(request, 'news/category_list.html', context)


def show_country(request, country_name):
    try:
        country = Country.objects.get(name=country_name)
        articles = Article.objects.filter(country=country)
    except Country.DoesNotExist:
        country = None
        articles = []

    latest_article = articles.first()
    other_articles = articles[1:]

    if latest_article:
        latest_article.views += 1  # Увеличиваем счетчик просмотров
        latest_article.save()

    context = {
        'country': country,
        'latest_article': latest_article,
        'other_articles': other_articles,
        'articles': articles,
    }

    return render(request, 'news/category_list.html', context)


class AuthorListView(ListView):
    model = Author
    articles = Article.objects.all().order_by('-pub_date')

    template_name = 'News/all_news.html'  # Создайте этот шаблон



class ArticleListView(ListView):
    model = Article
    template_name = 'news/all_news.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-pub_date')

        # Получаем параметр article_id из URL
        article_id = self.request.GET.get('article_id')

        if article_id:
            # Получаем выбранную статью по article_id
            selected_article = queryset.filter(pk=article_id).first()

            # Если есть выбранная статья, пересортируем список
            if selected_article:
                queryset = sorted(queryset, key=lambda article: article == selected_article, reverse=True)

                # Увеличиваем счетчик просмотров выбранной статьи
                selected_article.views += 1
                selected_article.save()

        return queryset





def index(request):
    articles = Article.objects.all().order_by('-pub_date')
    countries = Country.objects.all()
    latest_article = articles.first()
    other_articles = articles[1:]
    categories = Category.objects.all()
    articles_by_category = {}
    prefetch_articles = Prefetch('article_set', queryset=Article.objects.all())
    categories = categories.prefetch_related(prefetch_articles)

    for idx, country in enumerate(countries):
        countries[idx].dative_name = add_dative_ending_russian(country.name)  # Добавляем поле с именем в дательном падеже

    for category in categories:
        articles_by_category[category] = category.article_set.all()

    context = {
        'latest_article': latest_article,
        'other_articles': other_articles,
        'articles': articles,
        'articles_by_category': articles_by_category,
        'countries': countries,
        'category': category,
    }
    return render(request, 'news/index.html', context)



def articles_by_category(request):
    categories = Category.objects.all()

    context = {'categories': categories}
    return render(request, 'news/index.html', context)



morph = pymorphy2.MorphAnalyzer()

def to_dative_case_russian(word):
    parsed_word = morph.parse(word)[0]
    dative_word = parsed_word.inflect({'datv'}).word
    return dative_word


def add_dative_ending_russian(text):
    country_name = text
    dative_country = to_dative_case_russian(country_name)
    return f'{country_name + "e" if country_name.endswith("стан") else dative_country}'
