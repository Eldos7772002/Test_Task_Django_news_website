# Generated by Django 3.2 on 2023-08-11 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0004_country_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
