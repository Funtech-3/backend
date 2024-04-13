from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    Serializer,
    SerializerMethodField,
)

from .models import City, NotificationSwitch, Tag

User = get_user_model()


class TagsSerializer(Serializer):
    """Сериализатор для тегов на главную страницу и
    в личном кабинете пользователя.
    """

    id = PrimaryKeyRelatedField(read_only=True)
    title = CharField()

    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
        )


class CitiesSerializer(Serializer):
    """Сериализатор для городов на главную страницу и
    в личном кабинете пользователя.
    """

    id = PrimaryKeyRelatedField(read_only=True)
    name = CharField()

    class Meta:
        model = City
        fields = (
            "id",
            "name",
        )


class CustomUserSerializer(ModelSerializer):
    """Сериализатор кастомноой модели пользователя,
    с использованием JSON ЯндексID.
    """

    yandex_id = IntegerField()
    full_name = SerializerMethodField()
    tags = TagsSerializer(many=True, read_only=True)
    cities = CitiesSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "yandex_id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "telegram_username",
            "position",
            "work_place",
            "tags",
            "cities",
            "avatar",
            "full_name",
        )
        read_only_fields = (
            "id",
            "tags",
            "cities",
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.telegram_username = validated_data.get(
            "telegram_username", instance.telegram_username
        )
        instance.position = validated_data.get("position", instance.position)
        instance.work_place = validated_data.get(
            "work_place", instance.work_place
        )
        instance.save()
        return instance

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class NotificationSwitchSerializer(ModelSerializer):
    """Сериализатор переключателей уведомлений для пользователя."""

    yandex_id = ReadOnlyField(source="user.yandex_id", read_only=True)

    class Meta:
        model = NotificationSwitch
        fields = (
            "yandex_id",
            "is_notification",
            "is_email",
            "is_telegram",
            "is_phone",
            "is_push",
        )

    def update(self, instance, validated_data):
        instance.is_notification = validated_data.get(
            "is_notification", instance.is_notification
        )
        instance.is_email = validated_data.get("is_email", instance.is_email)
        instance.is_telegram = validated_data.get(
            "is_telegram", instance.is_telegram
        )
        instance.is_phone = validated_data.get("is_phone", instance.is_phone)
        instance.is_push = validated_data.get("is_push", instance.is_push)
        instance.save()
        return instance


class InterestsSerializer(Serializer):
    """Сериализатор интересов пользователя,
    показывает интересные теги и города в личном кабинете.
    """

    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    cities = PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        many=True,
    )

    class Meta:
        model = User
        fields = (
            "tags",
            "cities",
        )

    def update(self, instance, validated_data):
        tags_data = validated_data.get("tags", [])
        cities_data = validated_data.get("cities", [])
        instance.tags.clear()
        instance.cities.clear()

        for tags in tags_data:
            tag = Tag.objects.get(id=tags.id)
            instance.tags.add(tag)

        for cities in cities_data:
            city = City.objects.get(id=cities.id)
            instance.cities.add(city)

        instance.save()
        return instance
