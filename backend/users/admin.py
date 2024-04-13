from django.contrib import admin
from django.contrib.auth import get_user_model
from tickets.models import Registration

from .constants import LIMIT_POSTS_PER_PAGE
from .models import City, NotificationSwitch, Tag

User = get_user_model()

admin.site.empty_value_display = "Не задано"
admin.site.site_header = "Администрирование проекта 'Funtech(Яндекс.События)'"
admin.site.site_title = "Портал администраторов 'Funtech'"
admin.site.index_title = (
    "Добро пожаловать, здесь можно найти мероприятие по душе!"
)


class RegistrationInline(admin.TabularInline):
    """Вложенное отображение для модели Registration."""

    model = Registration
    fields = (
        "status",
        "event",
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка отображения для кастомной модели User."""

    inlines = [RegistrationInline]
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
    )
    list_editable = (
        "first_name",
        "last_name",
    )
    list_filter = (
        "username",
        "email",
        "phone_number",
        "last_name",
    )
    search_fields = (
        "username",
        "email",
        "phone_number",
    )
    list_display_links = (
        "username",
        "email",
        "phone_number",
    )
    ordering = ("username",)
    list_per_page = LIMIT_POSTS_PER_PAGE

    fieldsets = (
        (None, {"fields": ("username", "yandex_id")}),
        (
            "Персональные данные",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "telegram_username",
                    "position",
                    "work_place",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(NotificationSwitch)
class NotificationsAdmin(admin.ModelAdmin):
    """Настройка отображения для кастомной модели User."""

    list_display = (
        "is_notification",
        "is_email",
        "is_telegram",
        "is_phone",
        "is_push",
        "user",
    )
    list_editable = ("is_email", "is_telegram", "is_phone", "is_push", "user")
    ordering = ("id",)
    list_per_page = LIMIT_POSTS_PER_PAGE


admin.site.register(Tag)
admin.site.register(City)
