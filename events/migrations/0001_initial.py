# Generated by Django 5.0.4 on 2024-04-10 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название города')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'города',
            },
        ),
        migrations.CreateModel(
            name='EventStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('start_time', models.TimeField(verbose_name='Начало этапа')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Этап события',
                'verbose_name_plural': 'этапы события',
                'ordering': ('start_time',),
                'default_related_name': 'steps',
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Название типа')),
            ],
            options={
                'verbose_name': 'Тип события',
                'verbose_name_plural': 'типы событий',
            },
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('work_place', models.CharField(max_length=256, verbose_name='Место работы')),
                ('position', models.CharField(max_length=256, verbose_name='Должность')),
                ('image', models.ImageField(blank=True, upload_to='events/images/speakers', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Спикер',
                'verbose_name_plural': 'спикеры',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.CharField(max_length=150, unique=True, verbose_name='Символьный код')),
                ('address', models.CharField(max_length=150, verbose_name='Адрес')),
                ('date', models.DateField(null=True, verbose_name='Дата проведения')),
                ('registration_status', models.CharField(choices=[('OPEN', 'Регистрация открыта'), ('CLOSED', 'Регистрация завершена'), ('PENDING', 'Ожидание регистрации')], max_length=7, verbose_name='Статус регистрации')),
                ('mode', models.CharField(choices=[('ONLINE', 'Онлайн'), ('OFFLINE', 'Офлайн')], max_length=7, verbose_name='Формат проведения')),
                ('preview_image', models.ImageField(blank=True, null=True, upload_to='events/images/event/preview', verbose_name='Превью-фото события')),
                ('image', models.ImageField(upload_to='events/images/event/detail', verbose_name='Фото для страницы события')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.city', verbose_name='Город проведения')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'события',
                'ordering': ('-date', 'title'),
                'default_related_name': 'events',
            },
        ),
    ]
