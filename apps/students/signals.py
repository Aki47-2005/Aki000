from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.payments.models import Clearance

from .models import Student


@receiver(post_save, sender=Student)
def create_clearance(sender, instance, created, **kwargs):
    if created:
        Clearance.objects.get_or_create(student=instance)
