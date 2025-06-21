# leader_portal/urls.py

from django.urls import path
from . import views

app_name = "leader_portal"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/club/<int:pk>/edit/", views.edit_club, name="edit_club"),
    path("dashboard/club/<int:pk>/participants/",
         views.participants, name="participants"),
    path("dashboard/club/<int:pk>/apps/", views.manage_applications, name="manage_applications"),
    path("dashboard/club/<int:pk>/materials/",
         views.materials, name="materials"),
]
