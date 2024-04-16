from celery import shared_task
from django.db.models.signals import pre_save
from django.dispatch import receiver

from tickets.email_utils import send_ticket_info
from tickets.models import Registration


@shared_task
@receiver(pre_save, sender=Registration)
def registration_status_pre_save_signal(sender, instance, **kwargs):
    """Сигнал для модели Registration отслеживает событие перед сохранение.
    Если статус регистрации меняется на CONFIRMED
    """
    old_status = ""
    try:
        old_status = Registration.objects.get(pk=instance.pk).status
    except Registration.DoesNotExist:
        pass
    new_status = instance.status
    if (
        old_status != new_status
        and new_status == Registration.Status.CONFIRMED
    ):
        send_ticket_info(instance)
