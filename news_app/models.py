# news_app/models.py

from django.db import models
from django.urls import reverse
from django.conf import settings


class NewsItem(models.Model):
    NEWS_TYPE_CHOICES = [
        ("event", "Мероприятие"),
        ("report", "Отчет"),
        ("achievement", "Достижение"),
        ("announcement", "Объявление"),
    ]

    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("URL-идентификатор", max_length=200, unique=True)
    content = models.TextField("Содержимое")
    news_type = models.CharField("Тип", max_length=20, choices=NEWS_TYPE_CHOICES, default="announcement")
    club = models.ForeignKey(
        'main.Club',
        verbose_name="Кружок/Студия",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_items"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = models.ImageField("Изображение", upload_to="news/", blank=True)
    is_published = models.BooleanField("Опубликовано", default=False)
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)
    published_at = models.DateTimeField("Дата публикации", null=True, blank=True)

    class Meta:
        verbose_name = "Новость/Мероприятие"
        verbose_name_plural = "Новости и мероприятия"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_app:detail", kwargs={"slug": self.slug})
