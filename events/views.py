from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from tickets.models import Registration
from .filters import EventFilter

from .models import Event
from .serializers import EventDetailSerializer, EventPreviewSerializer


class EventViewSet(ReadOnlyModelViewSet):
    """Получение списка событий и конкретного события."""
    lookup_field = 'slug'
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'type__title']

    def get_queryset(self):
        if self.action == 'retrieve':
            return Event.objects.prefetch_related('tags', 'steps')
        return Event.objects.prefetch_related('tags')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventPreviewSerializer

    @action(
        detail=False,
        methods=[
            'POST',
        ],
        url_path=r'(?P<slug>[\w-]+)/registration',
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
