from django.urls import path
from . import views

app_name = 'student_portal'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/unsubscribe/<int:pk>/', views.unsubscribe, name='unsubscribe'),
    path('dashboard/review/<int:club_id>/', views.leave_review, name='leave_review'),
    path('dashboard/notifications/', views.notifications, name='notifications'),
]
