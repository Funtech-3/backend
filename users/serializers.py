from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор кастомноой модели юзер, с использованием JSON ЯндексID."""

    yandex_id = serializers.IntegerField()
    full_name = serializers.SerializerMethodField()

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
            "avatar",
            "full_name",
        )
        read_only_fields = ("id",)

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
        instance.tags = validated_data.get("tags", instance.tags)
        instance.save()
        return instance

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
