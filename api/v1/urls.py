from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from events.views import CityListView, EventViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path("", include(router_v1.urls)),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    path("", include("djoser.urls.authtoken")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("cities/", CityListView.as_view()),
]
