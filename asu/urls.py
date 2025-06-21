from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Админ-панель
    path('admin/', admin.site.urls),

    # Аутентификация
    path('accounts/', include('accounts.urls')),

    # Новости и мероприятия (news_app)
    path('news/', include('news_app.urls', namespace='news_app')),

    # Личный кабинет студента
    path('student/', include('student_portal.urls', namespace='student_portal')),

    # Основные публичные страницы
    path('', include('main.urls')),

    path("", include("leader_portal.urls", namespace="leader_portal")),

]

if settings.DEBUG:
    # Раздача медиа-файлов в режиме отладки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
