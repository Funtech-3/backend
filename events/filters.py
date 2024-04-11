from datetime import date

from django_filters import rest_framework as filters

from users.models import Tag
from .models import City, Event


class EventFilter(filters.FilterSet):
    """Фильтры для списка событий."""
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all()
    )
    city = filters.ModelMultipleChoiceFilter(
        queryset=City.objects.all()
    )
    date = filters.DateFromToRangeFilter()
    show_old = filters.BooleanFilter(method='filter_old')
    is_favorited = filters.BooleanFilter(method='filter_favorited')
    is_registrated = filters.BooleanFilter(
        method='filter_registrated'
    )

    class Meta:
        model = Event
        fields = (
            'tags',
            'city',
            'date',
            'show_old',
            'is_favorited',
            'is_registrated',
        )

    def filter_old(self, events, name, value):
        """Не показывать прошедшие или показать только прошедшие события."""
        if self.request is None:
            return Event.objects.none()
        today = date.today()
        if not value:
            return events.exclude(date__lt=today)
        return events.filter(date__lt=today)

    def filter_favorited(self, events, name, value):
        """
        Показать те события, которые добавлены
        или не добавлены в избранное.
        """
        if self.request is None:
            return Event.objects.none()
        user = self.request.user
        if not user.is_authenticated:
            return events
        if not value:
            return events.exclude(favorited_by=user)
        return events.filter(favorited_by=user)

    def filter_registrated(self, events, name, value):
        """
        Показать события, на которые зарегистрирован
        или не зарегестрирован пользователь.
        """
        if self.request is None:
            return Event.objects.none()
        user = self.request.user
        if not user.is_authenticated:
            return events
        if not value:
            return events.exclude(ticket_registrations__user=user)
        return events.filter(ticket_registrations__user=user)
