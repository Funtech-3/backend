from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from tickets.email_utils import send_ticket_info
from tickets.models import Registration
from users.models import NotificationSwitch


@receiver(pre_save, sender=Registration)
def watch_registration_status(sender, instance, **kwargs):
    print("Get pre_save model Registration signal.")
    is_notification = False
    is_email = False
    old_status = ""
    try:
        old_status = Registration.objects.get(pk=instance.pk).status
        if Registration.objects.get(pk=instance.pk):
            is_notification = Registration.objects.get(
                pk=instance.pk
            ).user.user_notifications.is_notification
            is_email = Registration.objects.get(
                pk=instance.pk
            ).user.user_notifications.is_email
    except (Registration.DoesNotExist, NotificationSwitch.DoesNotExist):
        pass
    new_status = instance.status
    if (
        old_status != new_status
        and new_status == Registration.Status.CONFIRMED
        and is_notification
        and is_email
    ):
        send_ticket_info(instance)
