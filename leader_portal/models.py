# leader_portal/models.py

from django.db import models
from main.models import Club


class Material(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField("Заголовок", max_length=200)
    file = models.FileField("Файл", upload_to="club_materials/")
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True)

    class Meta:
        verbose_name = "Материал клуба"
        verbose_name_plural = "Материалы клубов"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.club.name} — {self.title}"
