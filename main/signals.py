# main/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Application
from student_portal.models import Subscription

User = get_user_model()


@receiver(post_save, sender=Application)
def sync_subscription(sender, instance, **kwargs):
    """
    При изменении Application.status синхронизируем Subscription:
      - approved   → для каждого юзера с таким email создаём/активируем подписку;
      - rejected   → для каждого отменяем подписку;
      - pending    → тоже можно отменять (по желанию).
    """
    # выберем всех пользователей с тем же e-mail
    users = User.objects.filter(email__iexact=instance.email)
    if not users.exists():
        return

    for user in users:
        if instance.status == 'approved':
            Subscription.objects.update_or_create(
                user=user,
                club=instance.club,
                defaults={
                    'status': 'active',
                    'updated_at': timezone.now()
                }
            )
        else:
            Subscription.objects.filter(
                user=user,
                club=instance.club
            ).update(
                status='cancelled',
                updated_at=timezone.now()
            )
