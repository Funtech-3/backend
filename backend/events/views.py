from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from tickets.models import Registration

from .filters import EventFilter
from .models import Event
from .serializers import EventDetailSerializer, EventPreviewSerializer


EVENT_IN_FAVORITE = 'Событие {} уже есть в избранном.'
EVENT_NOT_IN_FAVORITE = 'Событие {} не добавлено в избранное.'


class EventViewSet(ReadOnlyModelViewSet):
    """Получение списка событий и конкретного события."""

    lookup_field = "slug"
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = EventFilter
    search_fields = ["title", "description", "type__title"]

    def get_queryset(self):
        if self.action == "retrieve":
            return Event.objects.prefetch_related("tags", "steps")
        return Event.objects.prefetch_related("tags")

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
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FavoriteView(APIView):
    """Добавление события в избранное или удаление события из избранного."""
    permission_classes = [IsAuthenticated]

    def post(self, request, event_slug):
        event = get_object_or_404(Event, slug=event_slug)
        user = request.user
        if user in event.favorited_by.all():
            raise ValidationError(
                {'errors': EVENT_IN_FAVORITE.format(event)}
            )
        event.favorited_by.add(user)
        return Response(
            EventDetailSerializer(event, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, event_slug):
        event = get_object_or_404(Event, slug=event_slug)
        user = request.user
        if user not in event.favorited_by.all():
            raise ValidationError(
                {'errors': EVENT_NOT_IN_FAVORITE.format(event)}
            )
        event.favorited_by.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
