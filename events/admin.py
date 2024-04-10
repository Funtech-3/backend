from django.contrib import admin

from .models import City, Event, EventStep, Tag, Speaker, EventType


class EventStepInline(admin.StackedInline):
    model = EventStep


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventStepInline]
    list_display = (
        'title',
        'city',
        'date'
    )


admin.site.register(EventType)
admin.site.register(City)
admin.site.register(Tag)
admin.site.register(Speaker)
