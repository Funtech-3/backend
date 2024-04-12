from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import City, NotificationSwitch, Tag
from .permissions import IsAuthenticatedAndOwner
from .serializers import (
    CitiesSerializer,
    CustomUserSerializer,
    InterestsSerializer,
    NotificationSwitchSerializer,
    TagsSerializer,
)

User = get_user_model()


class CustomUserViewSet(viewsets.ViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, pk=None):
        """Безопасный метод получения информации о юзере."""

        user = get_object_or_404(User, yandex_id=pk)
        serializer = self.serializer_class(user)
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        response_data = {
            "access_token": access_token,
            "refresh_token": str(refresh_token),
            "user": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
        # Cкорее всего никогда использоватсья не будет.

    def create(self, request):
        """Метод создания или получения юзера."""
        yandex_id = request.data.get("yandex_id")
        if yandex_id:
            user = User.objects.filter(yandex_id=yandex_id).first()
            if user:
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            username = request.data.get("login", None)
            email = request.data.get("default_email", None)
            phone_number = request.data.get("defaulte_phone", {}).get(
                "number", None
            )
            default_avatar_id = request.data.get("default_avatar_id", None)
            avatar_url = (
                f"https://avatars.yandex.net/get-yapic/{default_avatar_id}/"
            )
            user = User(
                yandex_id=yandex_id,
                username=username,
                email=email,
                phone_number=phone_number,
                avatar=avatar_url,
            )
            user.save()
            serializer = self.serializer_class(user)
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            response_data = {
                "access_token": access_token,
                "refresh_token": str(refresh_token),
                "user": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """метод обновления данных о юзере."""

        user = get_object_or_404(User, yandex_id=pk)
        serializer = self.serializer_class(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationsViewSet(viewsets.ModelViewSet):
    """Представление для уведомлений в личном кабинете юзера."""

    queryset = NotificationSwitch.objects.all().select_related("user")
    pagination_class = None
    serializer_class = NotificationSwitchSerializer
    permission_classes = (IsAuthenticatedAndOwner,)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class InterestsViewSet(viewsets.ModelViewSet):
    """Представление для тегов и городов в личном кабинете юзера."""

    serializer_class = InterestsSerializer
    permission_classes = (IsAuthenticatedAndOwner,)
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id).prefetch_related(
            "tags", "cities"
        )

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для тегов для главной страницы."""

    serializer_class = TagsSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class CitiesViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для тегов для главной страницы."""

    serializer_class = CitiesSerializer
    queryset = City.objects.all()
    pagination_class = None
