from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from users.views import CustomUserViewSet

router_v1 = routers.DefaultRouter()

router_v1.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(router_v1.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
