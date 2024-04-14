from http.client import BAD_REQUEST, CREATED, OK

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
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

        user = get_object_or_404(User, yandex_id=yandex_id)
        serializer = self.serializer_class(user)
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        response_data = {
            "access_token": access_token,
            "refresh_token": str(refresh_token),
            "user": serializer.data,
        }
        return Response(response_data, status=OK)

    def create(self, request):
        """Метод создания или получения пользователя."""

        data = request.data
        yandex_id = data.get("yandex_id")
        if yandex_id:
            user = User.objects.filter(yandex_id=yandex_id).first()
            if user:
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=OK)
            first_name = data.get("first_name", None)
            last_name = data.get("last_name", None)
            username = data.get("login", "username")
            email = data.get("default_email", "email")
            phone_number = data.get("defaulte_phone", {}).get(
                "number", "phone_number"
            )
            default_avatar_id = data.get("default_avatar_id", "avatar")
            avatar_url = (
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

        user = get_object_or_404(User, yandex_id=pk)
        serializer = self.serializer_class(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=OK)


class UserNotificationsAPIView(APIView):
    """Представление для уведомлений в личном кабинете пользователя."""

    serializer_class = NotificationSwitchSerializer

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
        notifications = self.get_notification_instance()
        serializer = NotificationSwitchSerializer(notifications)
        return Response(serializer.data, status=OK)

    def patch(self, request):
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

    serializer_class = InterestsSerializer
    permission_classes = (IsAuthenticatedAndOwner,)
    pagination_class = None

    def get_object(self):
        return self.request.user


class TagsListView(ListAPIView):
    """Представление тегов для главной страницы."""

    serializer_class = TagsSerializer
    queryset = Tag.objects.all()
    pagination_class = None

    def get_object(self):
        return self.request.user


class CitiesListView(ListAPIView):
    """Представление городов для главной страницы."""

    serializer_class = CitiesSerializer
    queryset = City.objects.all()
    pagination_class = None

    def get_object(self):
        return self.request.user
