# main/models.py
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField("Название категории", max_length=100)
    slug = models.SlugField("URL-идентификатор", max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


# main/models.py
from django.db import models
from django.urls import reverse
from django.conf import settings


class Club(models.Model):
    name = models.CharField("Название кружка/студии", max_length=150)
    slug = models.SlugField("URL-идентификатор", max_length=150, unique=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Руководитель (пользователь)",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="managed_clubs"
    )
    short_description = models.CharField("Краткое описание", max_length=255)
    description = models.TextField("Полное описание")
    logo = models.ImageField("Логотип", upload_to="clubs/", blank=True)
    schedule = models.TextField("Расписание занятий", blank=True)
    location = models.CharField("Место проведения", max_length=255, blank=True)
    leader_name = models.CharField("ФИО руководителя", max_length=150, blank=True)
    leader_contact = models.CharField("Контакты руководителя", max_length=255, blank=True)
    categories = models.ManyToManyField('Category', verbose_name="Категории", blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Кружок/Студия"
        verbose_name_plural = "Кружки и студии"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("club_detail", kwargs={"slug": self.slug})

    @property
    def active_subscriptions_count(self):
        """
        Возвращает количество активных подписок (статус='active') на этот кружок.
        """
        return self.subscriptions.filter(status='active').count()


class Application(models.Model):
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("approved", "Одобрено"),
        ("rejected", "Отклонено"),
    ]

    club = models.ForeignKey(
        Club,
        verbose_name="Кружок",
        on_delete=models.CASCADE,
        related_name="applications"
    )
    name = models.CharField("Имя заявителя", max_length=100)
    email = models.EmailField("Email заявителя")
    message = models.TextField("Сообщение", blank=True)
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default="pending")
    submitted_at = models.DateTimeField("Дата подачи", default=timezone.now)
    moderated_at = models.DateTimeField("Дата модерации", null=True, blank=True)

    class Meta:
        verbose_name = "Заявка на вступление"
        verbose_name_plural = "Заявки на вступление"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.club.name} – {self.name}"

class Location(models.Model):
    name = models.CharField("Название площадки", max_length=150, unique=True)
    address = models.CharField("Адрес", max_length=255, blank=True)

    class Meta:
        verbose_name = "Место проведения"
        verbose_name_plural = "Места проведения"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Leader(models.Model):
    name = models.CharField("ФИО руководителя", max_length=150, unique=True)
    email = models.EmailField("E-mail руководителя", blank=True)
    phone = models.CharField("Телефон руководителя", max_length=50, blank=True)

    class Meta:
        verbose_name = "Руководитель"
        verbose_name_plural = "Руководители"
        ordering = ["name"]

    def __str__(self):
        return self.name
