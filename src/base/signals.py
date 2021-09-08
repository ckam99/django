from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks.emails import send_confirmation_mail
from .models import User


@receiver(post_save, sender=User)
def user_save_handle(sender, instance, **kwargs):
    if instance.confirmed_at is None:
        return send_confirmation_mail(instance.email)
    pass
