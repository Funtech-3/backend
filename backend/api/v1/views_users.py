from http.client import BAD_REQUEST, CREATED, OK

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import City, NotificationSwitch, Tag
from users.permissions import IsAuthenticatedAndOwner
from users.serializers import (
    CitiesSerializer,
    CustomUserSerializer,
    InterestsSerializer,
    NotificationSwitchSerializer,
    TagsSerializer,
)

User = get_user_model()


class CustomUserViewSet(ViewSet):
    """Возвращает экземпляр пользователя, создает и изменяет.
    Используется ЯндексID для создания пользователя и токена.
    """

    serializer_class = CustomUserSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
    lookup_field = "yandex_id"

    def retrieve(self, request, yandex_id=None):
        """Безопасный метод получения информации о пользователе."""
        self.permission_classes = (IsAuthenticatedAndOwner,)

        user = get_object_or_404(User, yandex_id=yandex_id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=OK)

    def create(self, request):
        """Метод создания или получения пользователя."""

        data = request.data
        yandex_id = data.get("id") or data.get("yandex_id")
        if yandex_id:
            user = get_object_or_404(User, yandex_id=yandex_id)
            if user:
                serializer = self.serializer_class(user)
                refresh_token = RefreshToken.for_user(user)
                access_token = str(refresh_token.access_token)
                response_data = {
                    "access_token": access_token,
                    "refresh_token": str(refresh_token),
                    "user": serializer.data,
                }
                return Response(response_data, status=OK)
            first_name = data.get("first_name", None)
            last_name = data.get("last_name", None)
            username = data.get("login") or data.get("username")
            email = data.get("default_email") or data.get("email")
            phone_number = data.get("default_phone", {}).get(
                "number"
            ) or data.get("phone_number")
            default_avatar_id = data.get("default_avatar_id")
            avatar_url = data.get("avatar") or (
                f"https://avatars.yandex.net/get-yapic/{default_avatar_id}/"
            )
            telegram_username = data.get("telegram_username", None)
            position = data.get("position", None)
            work_place = data.get("work_place", None)
            user = User(
                yandex_id=yandex_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone_number=phone_number,
                avatar=avatar_url,
                telegram_username=telegram_username,
                position=position,
                work_place=work_place,
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
            return Response(response_data, status=CREATED)
        return Response(status=BAD_REQUEST)

    def update(self, request, pk=None):
        """Метод обновления данных о пользователе."""
        self.permission_classes = (IsAuthenticatedAndOwner,)

        user = get_object_or_404(User, yandex_id=pk)
        serializer = self.serializer_class(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=OK)


class UserNotificationsAPIView(APIView):
    """Представление для уведомлений в личном кабинете пользователя."""

    cache_time = 60 * 15
    serializer_class = NotificationSwitchSerializer
    permission_classes = (IsAuthenticatedAndOwner,)

    def get_cache_key(self):
        user_id = self.request.user.id
        return f"notifications_switch_{user_id}"

    def get_notification_instance(self):
        user = self.request.user
        notification, _ = NotificationSwitch.objects.get_or_create(
            user_id=user.id,
            defaults={
                "is_notification": False,
                "is_email": False,
                "is_telegram": False,
                "is_phone": False,
                "is_push": False,
            },
        )
        return notification

    def get(self, request):
        cache_data = cache.get(self.get_cache_key)
        if cache_data:
            return Response(cache_data, status=OK)
        notifications = self.get_notification_instance()
        serializer = NotificationSwitchSerializer(notifications)
        cache.set(self.get_cache_key, serializer.data, self.cache_time)
        return Response(serializer.data, status=OK)

    def patch(self, request):
        cache.delete(self.get_cache_key)
        user = get_object_or_404(User, id=self.request.user.id)
        notification = get_object_or_404(NotificationSwitch, user_id=user.id)
        serializer = NotificationSwitchSerializer(
            notification, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(user_id=user.id)
            return Response(serializer.data, status=OK)
        return Response(serializer.errors, status=BAD_REQUEST)


class UserInterestsAPIView(RetrieveUpdateAPIView):
    """Представление для тегов и городов в личном кабинете юзера."""

    cache_time = 60 * 15
    serializer_class = InterestsSerializer
    permission_classes = (IsAuthenticatedAndOwner,)
    pagination_class = None

    def get_cache_key(self):
        user_id = self.request.user.id
        return f"user_interests_{user_id}"

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        cache_data = cache.get(self.get_cache_key)
        if cache_data:
            return Response(cache_data, status=OK)
        response = super().get(request, *args, **kwargs)
        cache.set(self.get_cache_key, response.data, self.cache_time)
        return response

    def patch(self, request, *args, **kwargs):
        cache.delete(self.get_cache_key)
        return super().patch(request, *args, **kwargs)


class TagsListView(ListAPIView):
    """Представление тегов для главной страницы."""

    cache_key = "tags_list_key"
    cache_time = 60 * 120
    serializer_class = TagsSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = cache.get(self.cache_key)
        if not queryset:
            queryset = Tag.objects.all()
            cache.set(self.cache_key, queryset, self.cache_time)
        return queryset

    def get_object(self):
        return self.request.user


@receiver([post_save, post_delete], sender=Tag)
def invalidate_tag_cache(sender, instance, **kwargs):
    cache.delete("tags_list_key")


class CitiesListView(ListAPIView):
    """Представление городов для главной страницы."""

    cache_key = "cities_list_key"
    cache_time = 60 * 120
    serializer_class = CitiesSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = cache.get(self.cache_key)
        if not queryset:
            queryset = City.objects.all()
            cache.set(self.cache_key, queryset, self.cache_time)
        return queryset

    def get_object(self):
        return self.request.user


@receiver([post_save, post_delete], sender=City)
def invalidate_cities_cache(sender, instance, **kwargs):
    cache.delete("cities_list_key")
