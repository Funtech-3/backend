from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from events.views import CityListView, EventViewSet
from users.views import CustomUserViewSet
from tickets.views import UserTicketViewSet, EventRegistrationVieSet

router_v1 = routers.DefaultRouter()
router_v1.register("user/ticket", UserTicketViewSet, basename="ticket")
router_v1.register(r'events', EventViewSet, basename='event')
router_v1.register("ticket", EventRegistrationVieSet, basename="ticket")
router_v1.register("user", CustomUserViewSet, basename="user")

urlpatterns = [
    path("", include(router_v1.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("cities/", CityListView.as_view()),
]
