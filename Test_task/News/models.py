from django.db import models
from django.urls import reverse


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True, verbose_name='строка')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='country_images/')  # Добавляем поле для фотографии

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(verbose_name='Фото')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)  # Добавленное поле
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
