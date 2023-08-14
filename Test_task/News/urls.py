from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),


    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('articles/', views.ArticleListView.as_view(), name='article-list'),
    path('category/<str:category_name>/', views.show_category, name='show_category'),
    path('country/<str:country_name>/', views.show_country, name='show_country'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


