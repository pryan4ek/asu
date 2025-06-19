# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('leader', 'Руководитель'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(
        'Роль пользователя',
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
