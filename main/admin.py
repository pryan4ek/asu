from django.contrib import admin
from .models import Category, Club, Application
from django.utils import timezone


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
        now = timezone.now()
        for app in queryset:
            app.status = 'approved'
            app.moderated_at = now
            app.save()  # вызовет сигнал и создаст Subscription

    @admin.action(description="Отклонить выбранные заявки")
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')
