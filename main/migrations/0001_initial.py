# Generated by Django 5.2.1 on 2025-06-18 14:15

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL-идентификатор')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Leader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='ФИО руководителя')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail руководителя')),
                ('phone', models.CharField(blank=True, max_length=50, verbose_name='Телефон руководителя')),
            ],
            options={
                'verbose_name': 'Руководитель',
                'verbose_name_plural': 'Руководители',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название площадки')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Место проведения',
                'verbose_name_plural': 'Места проведения',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL-идентификатор')),
                ('content', models.TextField(verbose_name='Содержимое')),
                ('category', models.CharField(choices=[('news', 'Новость'), ('event', 'Событие')], default='news', max_length=10, verbose_name='Тип материала')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Одобрено админом')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Новость/Событие',
                'verbose_name_plural': 'Новости и события',
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название кружка/студии')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='URL-идентификатор')),
                ('short_description', models.CharField(max_length=255, verbose_name='Краткое описание')),
                ('description', models.TextField(verbose_name='Полное описание')),
                ('logo', models.ImageField(blank=True, upload_to='clubs/', verbose_name='Логотип')),
                ('schedule', models.TextField(blank=True, verbose_name='Расписание занятий')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='Место проведения')),
                ('leader_name', models.CharField(blank=True, max_length=150, verbose_name='Руководитель')),
                ('leader_contact', models.CharField(blank=True, max_length=255, verbose_name='Контакты руководителя')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('categories', models.ManyToManyField(blank=True, to='main.category', verbose_name='Категории')),
            ],
            options={
                'verbose_name': 'Кружок/Студия',
                'verbose_name_plural': 'Кружки и студии',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя заявителя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email заявителя')),
                ('message', models.TextField(blank=True, verbose_name='Сообщение')),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('approved', 'Одобрено'), ('rejected', 'Отклонено')], default='pending', max_length=10, verbose_name='Статус')),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата подачи')),
                ('moderated_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата модерации')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='main.club', verbose_name='Кружок')),
            ],
            options={
                'verbose_name': 'Заявка на вступление',
                'verbose_name_plural': 'Заявки на вступление',
                'ordering': ['-submitted_at'],
            },
        ),
    ]
