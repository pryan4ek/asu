from django.db import models
from django.conf import settings
from main.models import Club


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('active', 'Активна'),
        ('cancelled', 'Отменена'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='subscriptions')
    club = models.ForeignKey(Club,
                             on_delete=models.CASCADE,
                             related_name='subscriptions')
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Дата подписки', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        unique_together = ('user', 'club')
        verbose_name = 'Подписка студента'
        verbose_name_plural = 'Подписки студентов'

    def __str__(self):
        return f"{self.user.username} → {self.club.name} [{self.status}]"


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='reviews')
    club = models.ForeignKey(Club,
                             on_delete=models.CASCADE,
                             related_name='reviews')
    rating = models.PositiveSmallIntegerField('Оценка (1–5)', default=5)
    comment = models.TextField('Комментарий')
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)

    class Meta:
        unique_together = ('user', 'club')
        verbose_name = 'Отзыв студента'
        verbose_name_plural = 'Отзывы студентов'

    def __str__(self):
        return f"Отзыв {self.user.username} о {self.club.name}"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='notifications')
    message = models.CharField('Сообщение', max_length=255)
    link = models.URLField('Ссылка (опционально)', blank=True)
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}…"
