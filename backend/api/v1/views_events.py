from http.client import BAD_REQUEST, CREATED, NO_CONTENT, OK

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from events.filters import EventFilter
from events.models import Event
from events.serializers import EventDetailSerializer, EventPreviewSerializer
from tickets.models import Registration

EVENT_IN_FAVORITE = "Событие {} уже есть в избранном."
EVENT_NOT_IN_FAVORITE = "Событие {} не добавлено в избранное."


class EventViewSet(ReadOnlyModelViewSet):
    """Получение списка событий и конкретного события."""

    cache_key = "events_key"
    cache_time = 60 * 60
    lookup_field = "slug"
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = EventFilter
    search_fields = ["title", "description", "type__title"]

    def get_queryset(self):
        if self.action == "retrieve":
            queryset = Event.objects.prefetch_related("tags", "steps")
        queryset = Event.objects.prefetch_related("tags")

        cached_queryset = cache.get(self.cache_key)
        if cached_queryset:
            return cached_queryset
        else:
            cache.set(self.cache_key, queryset, self.cache_time)
            return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EventDetailSerializer
        return EventPreviewSerializer

    @action(
        detail=False,
        methods=[
            "POST",
        ],
        url_path=r"(?P<slug>[\w-]+)/registration",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def registration(self, request, **kwargs):
        """Зарегистрироваться на событие."""
        event = self.get_object()
        object, created = Registration.objects.get_or_create(
            user=self.request.user, event=event
        )
        if object:
            return Response(status=CREATED)
        return Response(status=BAD_REQUEST)


@receiver([post_save, post_delete], sender=Event)
def invalidate_event_cache(sender, instance, **kwargs):
    cache.delete(EventViewSet.cache_key)


class FavoriteView(APIView):
    """Добавление события в избранное или удаление события из избранного."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={201: EventDetailSerializer})
    def post(self, request, event_slug):
        """Добавить событие в избранное."""
        event = get_object_or_404(Event, slug=event_slug)
        user = request.user
        if user in event.favorited_by.all():
            raise ValidationError({"errors": EVENT_IN_FAVORITE.format(event)})
        event.favorited_by.add(user)
        return Response(
            EventDetailSerializer(event, context={"request": request}).data,
            status=CREATED,
        )

    def delete(self, request, event_slug):
        """Удалить событие из избранного."""
        event = get_object_or_404(Event, slug=event_slug)
        user = request.user
        if user not in event.favorited_by.all():
            raise ValidationError(
                {"errors": EVENT_NOT_IN_FAVORITE.format(event)}
            )
        event.favorited_by.remove(request.user)
        return Response(status=NO_CONTENT)
