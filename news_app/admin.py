# news_app/admin.py

from django.contrib import admin
from .models import NewsItem
from django.utils import timezone


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "news_type", "club", "is_published", "published_at")
    list_filter = ("news_type", "is_published", "club")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    actions = ("make_published",)

    @admin.action(description="Отметить как опубликованные")
    def make_published(self, request, queryset):
        now = timezone.now()
        queryset.update(is_published=True, published_at=now)
