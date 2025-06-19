# accounts/urls.py

from django.urls import path
from . import views
from .views import register, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
