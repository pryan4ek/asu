from django.contrib import admin
from .models import Category, Club, Application, News


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('categories',)
    search_fields = ('name', 'short_description')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('club', 'name', 'email', 'status', 'submitted_at')
    list_filter = ('status', 'club')
    actions = ('approve_applications', 'reject_applications')

    @admin.action(description="Одобрить выбранные заявки")
    def approve_applications(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description="Отклонить выбранные заявки")
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_approved', 'published_at')
    list_filter = ('category', 'is_approved')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    actions = ('approve_news',)

    @admin.action(description="Одобрить выбранные новости")
    def approve_news(self, request, queryset):
        queryset.update(is_approved=True, published_at=timezone.now())
