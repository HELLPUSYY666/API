from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .utils import send_notification_to_user


@receiver(post_save, sender=User)
def notify_user_on_creation(sender, instance, created, **kwargs):
    if created:
        send_notification_to_user(
            instance.user,
            "Новое событие",
            f"Объект {instance} был успешно создан!"
        )
