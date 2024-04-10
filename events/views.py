from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import EventFilter
from .models import City, Event
from .serializers import (
    CityReadSerializer,
    EventPreviewSerializer,
    EventDetailSerializer
)


class EventViewSet(ReadOnlyModelViewSet):
    """Получение списка событий и конкретного события."""
    lookup_field = 'slug'
    filterset_class = EventFilter

    def get_queryset(self):
        if self.action == 'retrieve':
            return Event.objects.prefetch_related('tags', 'steps')
        return Event.objects.prefetch_related('tags')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventPreviewSerializer


class CityListView(ListAPIView):
    """Получение списка городов."""
    queryset = City.objects.all()
    serializer_class = CityReadSerializer
