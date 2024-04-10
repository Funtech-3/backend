from datetime import date

from django_filters import rest_framework as filters

from users.models import Tag
from .models import City, Event


class EventFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__title',
        to_field_name='title',
        queryset=Tag.objects.all()
    )
    city = filters.ModelMultipleChoiceFilter(
        field_name='city__name',
        to_field_name='name',
        queryset=City.objects.all()
    )
    date = filters.DateFromToRangeFilter()
    show_old = filters.BooleanFilter(method='filter_old')
    is_favorited = filters.BooleanFilter(method='filter_favorited')

    class Meta:
        model = Event
        fields = (
            'tags',
            'city',
            'date',
            'show_old',
            'is_favorited',
        )

    def filter_old(self, events, name, value):
        if self.request is None:
            return Event.objects.none()
        today = date.today()
        if not value:
            return events.exclude(date__lt=today)
        return events.filter(date__lt=today)

    def filter_favorited(self, events, name, value):
        if self.request is None:
            return Event.objects.none()
        user = self.request.user
        if not user.is_authenticated:
            return events
        if not value:
            return events.exclude(favorited_by=user)
        return events.filter(favorited_by=user)
