from django.urls import path
from . import views
from .views import DashboardHomeView

urlpatterns = [
    # Публичные
    path("", views.index, name="index"),
    path("clubs/", views.clubs, name="clubs"),
    path('search/', views.clubs, name='search'),
    path("clubs/<slug:slug>/", views.club_detail, name="club_detail"),
    path("contacts/", views.contact, name="contact"),
    path("search/", views.search, name="search"),

    # Административная панель
    path("dashboard/", DashboardHomeView.as_view(), name="dashboard_home"),

    # Категории
    path("dashboard/categories/", views.CategoryListView.as_view(), name="dashboard_category_list"),
    path("dashboard/categories/add/", views.CategoryCreateView.as_view(), name="dashboard_category_add"),
    path("dashboard/categories/<int:pk>/edit/", views.CategoryUpdateView.as_view(), name="dashboard_category_edit"),
    path("dashboard/categories/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="dashboard_category_delete"),

    # Кружки/студии
    path("dashboard/clubs/", views.ClubListView.as_view(), name="dashboard_club_list"),
    path("dashboard/clubs/add/", views.ClubCreateView.as_view(), name="dashboard_club_add"),
    path("dashboard/clubs/<int:pk>/edit/", views.ClubUpdateView.as_view(), name="dashboard_club_edit"),
    path("dashboard/clubs/<int:pk>/delete/", views.ClubDeleteView.as_view(), name="dashboard_club_delete"),

    # Заявки
    path("dashboard/applications/", views.ApplicationListView.as_view(), name="dashboard_application_list"),
    path("dashboard/applications/<int:pk>/", views.ApplicationDetailView.as_view(),
         name="dashboard_application_detail"),
    path("dashboard/applications/<int:pk>/approve/", views.approve_application, name="dashboard_application_approve"),
    path("dashboard/applications/<int:pk>/reject/", views.reject_application, name="dashboard_application_reject"),

    # Статистика
    path("dashboard/stats/", views.dashboard_stats, name="dashboard_stats"),
]
