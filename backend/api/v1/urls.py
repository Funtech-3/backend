from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from events.views import EventViewSet
from rest_framework import routers
from tickets.views import UserTicketViewSet
from users.views import (
    CitiesListView,
    CustomUserViewSet,
    TagsListView,
    UserInterestsAPIView,
    UserNotificationsAPIView,
)

router_v1 = routers.DefaultRouter()
router_v1.register(r"events", EventViewSet, basename="event")
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
    path("", include(router_v1.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("tags/", TagsListView.as_view(), name="tags"),
    path("cities/", CitiesListView.as_view(), name="cities"),
]
