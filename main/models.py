from django.db import models
from django.urls import reverse
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


class Club(models.Model):
    name = models.CharField("Название кружка/студии", max_length=150)
    slug = models.SlugField("URL-идентификатор", max_length=150, unique=True)
    short_description = models.CharField("Краткое описание", max_length=255)
    description = models.TextField("Полное описание")
    logo = models.ImageField("Логотип", upload_to="clubs/", blank=True)
    schedule = models.TextField("Расписание занятий", blank=True)
    location = models.CharField("Место проведения", max_length=255, blank=True)
    leader_name = models.CharField("Руководитель", max_length=150, blank=True)
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
        return reverse('club_detail', kwargs={'slug': self.slug})


class Application(models.Model):
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("approved", "Одобрено"),
        ("rejected", "Отклонено"),
    ]
    club = models.ForeignKey(Club, verbose_name="Кружок", on_delete=models.CASCADE, related_name="applications")
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


class News(models.Model):
    CATEGORY_CHOICES = [
        ("news", "Новость"),
        ("event", "Событие"),
    ]
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("URL-идентификатор", max_length=200, unique=True)
    content = models.TextField("Содержимое")
    category = models.CharField("Тип материала", max_length=10, choices=CATEGORY_CHOICES, default="news")
    is_approved = models.BooleanField("Одобрено админом", default=False)
    created_at = models.DateTimeField("Дата создания", default=timezone.now)
    published_at = models.DateTimeField("Дата публикации", null=True, blank=True)

    class Meta:
        verbose_name = "Новость/Событие"
        verbose_name_plural = "Новости и события"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


from django.db import models
from django.urls import reverse


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
