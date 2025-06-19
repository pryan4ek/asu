# news_app/urls.py

from django.urls import path
from . import views

app_name = "news_app"

urlpatterns = [
    path("", views.NewsListView.as_view(), name="list"),
    path("events/", views.EventListView.as_view(), name="events"),
    path("<slug:slug>/", views.NewsDetailView.as_view(), name="detail"),
]
