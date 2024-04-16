# Generated by Django 5.0.4 on 2024-04-12 12:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tickets", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="registration",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Участник",
            ),
        ),
        migrations.AddConstraint(
            model_name="registration",
            constraint=models.UniqueConstraint(
                fields=("user", "event"), name="Unique_event_for_each_user"
            ),
        ),
    ]
