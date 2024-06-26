from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from .views_events import EventViewSet, FavoriteView
from .views_tickets import CheckTicketViewSet, UserTicketViewSet
from .views_users import (
    CitiesListView,
    CustomUserViewSet,
    TagsListView,
    UserInterestsAPIView,
    UserNotificationsAPIView,
)

router_v1 = routers.DefaultRouter()
router_v1.register(r"events", EventViewSet, basename="event")
router_v1.register(
    "user/ticket_check", CheckTicketViewSet, basename="ticket_check"
)
router_v1.register("user/ticket", UserTicketViewSet, basename="ticket")
router_v1.register("user", CustomUserViewSet, basename="user")


urlpatterns = [
    path(
        "user/interests/",
        UserInterestsAPIView.as_view(),
        name="interests",
    ),
    path(
        "user/notifications/",
        UserNotificationsAPIView.as_view(),
        name="user-notifications",
    ),
    path(
        "events/<str:event_slug>/favorite/",
        FavoriteView.as_view(),
        name="event-favorite",
    ),
    path("", include(router_v1.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("tags/", TagsListView.as_view(), name="tags"),
    path("cities/", CitiesListView.as_view(), name="cities"),
]
