from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

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


class Email(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

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


@receiver(pre_save, sender=Article)
def send_notification_email(sender, instance, **kwargs):
    if instance.pk is None:  # Проверяем, что статья создается, а не обновляется
        subject = 'Новая статья добавлена'
        message = f'Добавлена новая статья в КАЗПРЕСС: {instance.title}\nСсылка: example.com/articles/{instance.pk}/'
        from_email = 'mira070707@mail.ru'

        recipient_list = Email.objects.values_list('email', flat=True)

        send_mail(subject, message, from_email, recipient_list)



class ViewedArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)