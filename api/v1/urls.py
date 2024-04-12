from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from events.views import EventViewSet
from rest_framework import routers
from users.views import (
    CitiesViewSet,
    CustomUserViewSet,
    InterestsViewSet,
    NotificationsViewSet,
    TagsViewSet,
)

router_v1 = routers.DefaultRouter()
router_v1.register(r"events", EventViewSet, basename="event")
router_v1.register(
    "user/notifications", NotificationsViewSet, basename="notifications"
)
router_v1.register("user/interests", InterestsViewSet, basename="interests")
router_v1.register("user", CustomUserViewSet, basename="user")
router_v1.register("tags", TagsViewSet)
router_v1.register("cities", CitiesViewSet)

urlpatterns = [
    path("", include(router_v1.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
