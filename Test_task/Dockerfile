FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

# Выполняем создание суперпользователя после копирования файлов
RUN python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('Admin', 'admin@example.com', 'Admin')"
