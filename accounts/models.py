# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$',
                'Разрешены только буквы, цифры и символы @/./+/-/_'
            )
        ]
    )
    email = models.EmailField(
        'E-mail',
        unique=True,
        help_text='Обязательный. Уникальный адрес электронной почты.'
    )
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('leader', 'Руководитель'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )

    def save(self, *args, **kwargs):
        # нормализация e-mail
        self.email = self.email.lower()
        super().save(*args, **kwargs)
