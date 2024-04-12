from datetime import date

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Count
from django.utils.safestring import mark_safe

from .constants import IMAGE_HTML
from .models import Event, EventStep, EventType, Speaker


class PastUpcomingFilter(SimpleListFilter):
    title = 'По дате проведения'
    parameter_name = 'show_old'

    def lookups(self, request, model_admin):
        return (
            ('past', 'Прошедшие события'),
            ('upcoming', 'Предстоящие события')
        )

    def queryset(self, request, events):
        today = date.today()
        if self.value() == 'past':
            return events.filter(date__lt=today)
        if self.value() == 'upcoming':
            return events.filter(date__gte=today)


class EventStepInline(admin.StackedInline):
    model = EventStep


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventStepInline]
    list_display = (
        'title',
        'city',
        'type',
        'date',
        'preview_image_tag',
        'detail_image_tag',
        'registrated_count',
    )
    list_filter = (
        'tags__title',
        'mode',
        'registration_status',
        PastUpcomingFilter
    )
    search_fields = (
        'title',
        'city__name',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            registrated_count=Count('ticket_registrations')
        )

    @admin.display(description='Зарегистрировано пользователей',
                   ordering='registrated_count')
    def registrated_count(self, event):
        return event.registrated_count

    @admin.display(description='Картинка превью')
    @mark_safe
    def preview_image_tag(self, event):
        if not event.preview_image:
            return '-'
        return IMAGE_HTML.format(event.preview_image.url)

    @admin.display(description='Картинка общая')
    @mark_safe
    def detail_image_tag(self, event):
        return IMAGE_HTML.format(event.image.url)


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'work_place',
        'position',
        'image_tag'
    )
    search_fields = ('work_place', 'position')

    @admin.display(description='Имя и фамилия')
    def full_name(self, speaker):
        return speaker.full_name

    @admin.display(description='Портрет')
    @mark_safe
    def image_tag(self, speaker):
        if not speaker.image:
            return '-'
        return IMAGE_HTML.format(speaker.image.url)


admin.site.register(EventType)
