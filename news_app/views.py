# news_app/views.py

from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import NewsItem


class NewsListView(ListView):
    model = NewsItem
    template_name = "news_app/news_list.html"
    context_object_name = "news_list"
    paginate_by = 10

    def get_queryset(self):
        return NewsItem.objects.filter(is_published=True).order_by("-published_at")


class EventListView(ListView):
    model = NewsItem
    template_name = "news_app/event_list.html"
    context_object_name = "events"
    paginate_by = 10

    def get_queryset(self):
        return NewsItem.objects.filter(
            is_published=True,
            news_type="event"
        ).order_by("published_at")  # события по возрастанию даты


class NewsDetailView(DetailView):
    model = NewsItem
    template_name = "news_app/news_detail.html"
    context_object_name = "news"
