# Generated by Django 3.2 on 2023-08-14 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0010_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='Фото'),
        ),
    ]
