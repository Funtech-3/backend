from rest_framework import serializers

from users.serializers import TagsSerializer
from .models import Event, EventStep, Speaker


class SpeakerReadSerializer(serializers.ModelSerializer):
    """Сериализатор спикера."""

    speaker_id = serializers.CharField(source="id", read_only=True)
    speaker_name = serializers.CharField(source="full_name", read_only=True)

    class Meta:
        model = Speaker
        fields = (
            "speaker_id",
            "speaker_name",
            "work_place",
            "position",
            "image",
        )
        read_only_fields = fields


class StepReadSerializer(serializers.ModelSerializer):
    """Сериализатор этапа события."""

    speakers = SpeakerReadSerializer(many=True, read_only=True)

    class Meta:
        model = EventStep
        fields = ("start_time", "title", "description", "speakers")
        read_only_fields = fields


class EventPreviewSerializer(serializers.ModelSerializer):
    """Сериалиазатор события с краткой информацией."""

    event_id = serializers.IntegerField(source="id", read_only=True)
    city = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )
    tags = TagsSerializer(
        many=True,
        read_only=True,
    )
    name = serializers.CharField(
        source="title",
        read_only=True,
    )
    date_event = serializers.DateField(
        source="date",
        read_only=True,
    )
    is_in_favorites = serializers.SerializerMethodField(read_only=True)
    is_registrated = serializers.SerializerMethodField(read_only=True)
    user_registration_status = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Event
        fields = (
            "event_id",
            "slug",
            "name",
            "description",
            "city",
            "date_event",
            "registration_status",
            "tags",
            "preview_image",
            "is_in_favorites",
            "is_registrated",
            "user_registration_status",
        )
        read_only_fields = fields

    def get_is_in_favorites(self, event: Event) -> bool:
        user = self.context["request"].user
        return (
            user.is_authenticated
            and user.favorite_events.filter(pk=event.pk).exists()
        )

    def get_is_registrated(self, event: Event) -> bool:
        user = self.context["request"].user
        return (
            user.is_authenticated
            and user.ticket_registrations.filter(event=event).exists()
        )

    def get_user_registration_status(self, event: Event) -> str:
        user = self.context["request"].user
        if not user.is_authenticated:
            return ""
        registrations = user.ticket_registrations.filter(event=event)
        if registrations:
            return registrations[0].status
        return ""


class EventDetailSerializer(EventPreviewSerializer):
    """Сериализатор события с подробной информацией."""

    event_type = serializers.SlugRelatedField(
        source="type", read_only=True, slug_field="title"
    )
    event_program = StepReadSerializer(
        source="steps", read_only=True, many=True
    )
    event_detail_image = serializers.ImageField(source="image", read_only=True)
    event_format = serializers.CharField(source="mode", read_only=True)
    event_description = serializers.CharField(
        source="description", read_only=True
    )

    class Meta:
        model = Event
        fields = (
            "event_id",
            "slug",
            "name",
            "city",
            "address",
            "date_event",
            "registration_status",
            "tags",
            "event_detail_image",
            "event_description",
            "event_type",
            "event_format",
            "event_program",
            "is_in_favorites",
            "is_registrated",
            "user_registration_status",
        )
        read_only_fields = fields
